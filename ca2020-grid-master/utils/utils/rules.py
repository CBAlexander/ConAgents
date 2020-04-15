from typing import Dict, Callable

from business_rules.actions import BaseActions
from business_rules.engine import check_conditions_recursively
from business_rules.fields import FIELD_NO_INPUT, FIELD_NUMERIC, FIELD_TEXT, FIELD_SELECT, FIELD_SELECT_MULTIPLE
from business_rules.operators import export_type, BaseType, type_operator
from business_rules.utils import fn_name_to_pretty_label
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, _rule_variable_wrapper
from utils.abstract_classes import Response
from utils.dict_query import DictQuery

FIELD_DICT = "dict"
FIELD_BOOLEAN = "boolean"


@export_type
class DictType(BaseType):
    name = "dict"

    def _assert_valid_value_and_cast(self, value):
        value = value or {}

        if not isinstance(value, dict):
            raise AssertionError("{0} is not a valid dict type.".
                                 format(value))

        return value

    @type_operator(FIELD_DICT)
    def equal_to(self, other_dict):
        return self.value == other_dict

    @type_operator(FIELD_NO_INPUT)
    def non_empty(self):
        return bool(self.value)

    @type_operator(FIELD_TEXT)
    def contains(self, key):
        return key in self.value


def dict_rule_variable(label=None):
    return _rule_variable_wrapper(DictType, label)


# Defines common variables for the condition part of the rules
class StateVariables(BaseVariables):

    def __init__(self, state, bot_name=None):
        self.state = DictQuery(state)
        self.bot_name = bot_name

    @string_rule_variable
    def processed_text(self):
        return self.state.get("current_state.state.nlu.annotations.processed_text")

    @string_rule_variable
    def intent(self):
        return self.state.get("current_state.state.nlu.annotations.intents.intent")

    @string_rule_variable
    def topic(self):
        return self.state.get("current_state.state.nlu.annotations.topics")

    @numeric_rule_variable
    def asr_confidence(self):
        best_hyp = self.state.get("current_state.state.input.hypotheses")[0]

        return best_hyp["confidence"]

    @dict_rule_variable
    def ner(self):
        return self.state.get("current_state.state.nlu.annotations.ner")

    @dict_rule_variable
    def entity_linking(self):
        return self.state.get("current_state.state.nlu.annotations.entity_linking")

    @dict_rule_variable
    def bot_params(self):
        if self.bot_name:
            bot_states = self.state.get("current_state.state.bot_states")

            return bot_states[self.bot_name]
        else:
            return {}

    @string_rule_variable
    def last_bot(self):
        return self.state.get("current_state.state.last_bot")


def _validate_action_parameters(func, params):
    """ Verifies that the parameters specified are actual parameters for the
    function `func`, and that the field types are FIELD_* types in fields.
    """
    if params is not None:
        # Verify field name is valid
        valid_fields = [
            FIELD_TEXT,
            FIELD_NUMERIC,
            FIELD_NO_INPUT,
            FIELD_SELECT,
            FIELD_SELECT_MULTIPLE,
            FIELD_DICT,
            FIELD_BOOLEAN
        ]

        for param in params:
            param_name, field_type = param['name'], param['fieldType']
            if param_name not in func.__code__.co_varnames:
                raise AssertionError("Unknown parameter name {0} specified for" \
                                     " action {1}".format(
                    param_name, func.__name__))

            if field_type not in valid_fields:
                raise AssertionError("Unknown field type {0} specified for" \
                                     " action {1} param {2}".format(
                    field_type, func.__name__, param_name))


def rule_action(label=None, state=None, response=None, params=None):
    """ Decorator to make a function into a rule action
    """

    def wrapper(func):
        params_ = params
        if isinstance(params, dict):
            params_ = [dict(label=fn_name_to_pretty_label(name),
                            name=name,
                            fieldType=field_type) \
                       for name, field_type in params.items()]
        _validate_action_parameters(func, params_)
        func.is_rule_action = True
        func.label = label \
                     or fn_name_to_pretty_label(func.__name__)
        func.params = params_
        return func

    return wrapper


class RuleEngine:
    def __init__(self, bot_name: str, rules: Dict, state_class: Callable, actions: BaseActions):
        self.bot_name = bot_name
        self.rules = rules
        self.defined_actions = actions
        self.state_class = state_class

    def step(self, state: Dict, stop_on_first_trigger: bool = True):
        """
        Execute all the actions triggered by the current state. If needed, it will execute the actions associated to the
        first matching rule.

        :param: bot_name: name of the bot that it's using the rule engine
        :param state: current state of the world
        :param stop_on_first_trigger: Execute only the first matching action
        :return: True if a rule fired, False otherwise
        """
        # always re-initialise the state
        return self.run_all(
            state=state,
            stop_on_first_trigger=stop_on_first_trigger
        )

    def run_all(self,
                state,
                stop_on_first_trigger=False):
        state = DictQuery(state)
        defined_variables = self.state_class(state, self.bot_name)

        final_response = Response()
        final_response.bot_name = self.bot_name
        final_response.bot_params = state.get("current_state.state.bot_states", {}).get(self.bot_name, {}).get(
            "bot_attributes", {})

        rule_was_triggered = False
        for rule in self.rules:
            curr_response = self.run(state, final_response, rule, defined_variables, self.defined_actions)
            if curr_response is not None:
                final_response = curr_response
                rule_was_triggered = True
                # check if we want to stop after the first matching rule
                if stop_on_first_trigger:
                    return final_response, True
        return final_response, rule_was_triggered

    def run(self, state, response, rule, defined_variables, defined_actions):
        conditions, actions = rule['conditions'], rule['actions']
        rule_triggered = check_conditions_recursively(conditions, defined_variables)
        if rule_triggered:
            response = self.do_actions(state, response, actions, defined_actions)
            return response
        return None

    def do_actions(self, state, response, actions, defined_actions):
        for action in actions:
            method_name = action['name']

            def fallback(*args, **kwargs):
                raise AssertionError("Action {0} is not defined in class {1}" \
                                     .format(method_name, defined_actions.__class__.__name__))

            params = action.get('params') or {}
            method = getattr(defined_actions, method_name, fallback)
            response = method(state, response, **params)

        return response
