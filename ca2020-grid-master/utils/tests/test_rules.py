import json
from typing import Dict

from business_rules.actions import BaseActions
from utils.rules import RuleEngine, rule_action, StateVariables, FIELD_BOOLEAN


class SimpleActions(BaseActions):
    """
    Every action should return a tuple containing:
    - Updated state
    - Response

    StateActions represents an abstract class for the bot behaviour. Multiple actions can be associated to the bot.
    The actual policy for the bot should be specified in the bot rules that defines the mapping between a given
    state and a given action.
    """

    @rule_action()
    def print_state(self, state, response) -> Dict:
        print("State: {}".format(state))
        return response

    @rule_action()
    def update_bot_params_with_topic(self, state, response) -> Dict:
        response.bot_params["topics"] = state.get("current_state.state.nlu.annotations.topics")
        return response

    @rule_action()
    def update_bot_params_with_ner(self, state, response) -> Dict:
        response.bot_params["ner"] = state.get("current_state.state.nlu.annotations.ner")
        return response

    @rule_action(params={"is_multi_turn": FIELD_BOOLEAN})
    def func_with_bool_param(self, state, response, is_multi_turn) -> Dict:
        response.bot_params["is_multi_turn"] = is_multi_turn
        return response


class TestRules:
    def test_change_topic(self):
        rules = json.loads(
            """
               [
                 {
                   "conditions": {
                     "all": [
                       {
                         "name": "intent",
                         "operator": "equal_to",
                         "value": "tell_me_about"
                       }
                     ]
                   },
                   "actions": [
                     {
                       "name": "update_bot_params_with_topic"
                     }
                   ]
                 }
               ]
        """)

        engine = RuleEngine("test_bot", rules, StateVariables, SimpleActions())

        state = {
            "current_state": {
                "state": {
                    "nlu": {
                        "annotations": {
                            "intents": {"intent": "tell_me_about", "param": "George Clooney"},
                            "topics": "movies",
                            "ner": {
                                "PERSON": ["George Clooney"]
                            },
                            "processed_text": "tell me about George Clooney"
                        }
                    },
                    "input": {
                        "hypotheses": [
                            {
                                "confidence": 0.6
                            }
                        ]
                    }
                }
            }
        }

        response, is_triggered_rule = engine.step(state)

        if is_triggered_rule:
            print("State: {}".format(state))
            print("Response: {}".format(response))
        else:
            assert "No rule fired -- something is wrong either with the state definition or with the rules"

        assert response.bot_params["topics"] == "movies"

    def test_noempty_ner(self):
        rules = json.loads(
            """
               [
                 {
                   "conditions": {
                     "all": [
                       {
                         "name": "intent",
                         "operator": "equal_to",
                         "value": "tell_me_about"
                       },
                       {
                         "name": "ner",
                         "operator": "non_empty",
                         "value": {}
                       }
                     ]
                   },
                   "actions": [
                     {
                       "name": "update_bot_params_with_ner"
                     }
                   ]
                 }
               ]
        """)

        engine = RuleEngine("test_bot", rules, StateVariables, SimpleActions())

        state = {
            "current_state": {
                "state": {
                    "nlu": {
                        "annotations": {
                            "intents": {"intent": "tell_me_about", "param": "George Clooney"},
                            "topics": "movies",
                            "ner": {
                                "PERSON": ["George Clooney"]
                            },
                            "processed_text": "tell me about George Clooney"
                        }
                    },
                    "input": {
                        "hypotheses": [
                            {
                                "confidence": 0.6
                            }
                        ]
                    }
                }
            }
        }

        response, is_triggered_rule = engine.step(state)

        if is_triggered_rule:
            print("State: {}".format(state))
            print("Response: {}".format(response))
        else:
            assert "No rule fired -- something is wrong either with the state definition or with the rules"

        assert response.bot_params.get("ner", None) is not None

    def test_empty_ner(self):
        rules = json.loads(
            """
               [
                 {
                   "conditions": {
                     "all": [
                       {
                         "name": "intent",
                         "operator": "equal_to",
                         "value": "tell_me_about"
                       },
                       {
                         "name": "ner",
                         "operator": "non_empty",
                         "value": {}
                       }
                     ]
                   },
                   "actions": [
                     {
                       "name": "update_bot_params_with_ner"
                     }
                   ]
                 }
               ]
        """)

        engine = RuleEngine("test_bot", rules, StateVariables, SimpleActions())

        state = {
            "current_state": {
                "state": {
                    "nlu": {
                        "annotations": {
                            "intents": {"intent": "tell_me_about", "param": "George Clooney"},
                            "topics": "movies",
                            "processed_text": "tell me about George Clooney"
                        }
                    },
                    "input": {
                        "hypotheses": [
                            {
                                "confidence": 0.6
                            }
                        ]
                    }
                }
            }
        }

        response, is_triggered_rule = engine.step(state)

        assert not is_triggered_rule

    def test_multiple_actions(self):
        rules = json.loads(
            """
               [
                 {
                   "conditions": {
                     "all": [
                       {
                         "name": "intent",
                         "operator": "equal_to",
                         "value": "tell_me_about"
                       }
                     ]
                   },
                   "actions": [
                     {
                       "name": "update_bot_params_with_ner"
                     },
                     {
                        "name": "update_bot_params_with_topic"
                     }
                   ]
                 }
               ]
        """)

        engine = RuleEngine("test_bot", rules, StateVariables, SimpleActions())

        state = {
            "current_state": {
                "state": {
                    "nlu": {
                        "annotations": {
                            "intents": {"intent": "tell_me_about", "param": "George Clooney"},
                            "topics": "movies",
                            "processed_text": "tell me about George Clooney",
                            "ner": {
                                "PERSON": ["George Clooney"]
                            }
                        }
                    },
                    "input": {
                        "hypotheses": [
                            {
                                "confidence": 0.6
                            }
                        ]
                    }
                }
            }
        }

        response, is_triggered_rule = engine.step(state)

        assert "topics" in response.bot_params and "ner" in response.bot_params

        print("Updated bot parameters: {}".format(response.bot_params))

    def test_boolean_param(self):
        rules = json.loads(
            """
               [
                 {
                   "conditions": {
                     "all": [
                       {
                         "name": "intent",
                         "operator": "equal_to",
                         "value": "tell_me_about"
                       }
                     ]
                   },
                   "actions": [
                     {
                       "name": "update_bot_params_with_ner"
                     },
                     {
                        "name": "update_bot_params_with_topic"
                     },
                     {
                        "name": "func_with_bool_param",
                        "params": {
                            "is_multi_turn": false
                        }
                     }
                   ]
                 }
               ]
        """)

        engine = RuleEngine("test_bot", rules, StateVariables, SimpleActions())

        state = {
            "current_state": {
                "state": {
                    "nlu": {
                        "annotations": {
                            "intents": {"intent": "tell_me_about", "param": "George Clooney"},
                            "topics": "movies",
                            "processed_text": "tell me about George Clooney",
                            "ner": {
                                "PERSON": ["George Clooney"]
                            }
                        }
                    },
                    "input": {
                        "hypotheses": [
                            {
                                "confidence": 0.6
                            }
                        ]
                    }
                }
            }
        }

        response, is_triggered_rule = engine.step(state)

        assert response.bot_params["is_multi_turn"] is not None
