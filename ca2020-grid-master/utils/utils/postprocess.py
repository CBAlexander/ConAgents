#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import random
import re
import yaml


class Postprocessor(object):
    """A simple response post-processing object."""

    def __init__(self, rule_file):
        """Load postprocessing rules from a YAML file.
        @param intents_file: path to the intents YAML file
        """
        # Read rules from file
        with codecs.open(rule_file, 'r', 'UTF-8') as fh:
            rules_data = yaml.load(fh)

        self.rules = rules_data

    def _replace_entities(self, text, context, entities):
        """Replace '*that*' for named entities in the given text"""
        if '*that*' not in text:
            return text
        # "entities" only holds one preselected entity -> replace it always
        if isinstance(entities, str):
            if entities != "":
                return text.replace('*that*', entities)
            else:
                return text.replace('*that*', 'that')
        # "entities" is a dict with more entities -> search for them in context & replace if found
        replacement = None
        for entity in [entity for etype in ['persons', 'locations', 'organizations']
                       for entity in entities[etype]]:
            # try to find the recent entity in the actual text
            entity_occ_pattern = re.escape(entity)
            if entity.count(' ') == 1:  # allow middle names for name + surname
                entity_occ_pattern = ' (\w+ ){0,3}'.join(entity.split(' '))
            entity_occ_pattern += r'(?! said)'  # ignore spokespeople
            if re.search(entity_occ_pattern, context, re.IGNORECASE):
                replacement = entity
                break
        if replacement:
            return text.replace('*that*', replacement)
        else:
            return text.replace('*that*', 'that')

    def postprocess(self, case, response, entities, context='', username=''):
        """Main function: postprocess the given system response based
        on the loaded rules, using information about the user question and named entities
        and a "case" tag (which is whatever you define in the rules file).

        @param case: a tag preselecting which rules may trigger
        @param response: the system response to postprocess
        @param question: the preceding user question
        @param entities: all named entities found in the user question, or a single entity \
            that should be replaced
        @param context: the user question (may be left blank)
        @return: the postprocessed response
        """
        sent_len = response.count(' ') + 1
        orig_resp = response

        # apply all rules
        for rule in self.rules:
            # rule applies to current case (or all cases)
            if 'cases' not in rule or case in rule['cases']:
                # only apply the rule with a given probability
                if 'probability' in rule and random.random() > rule['probability']:
                    continue
                # length limitation: ignore sentences that do not comply
                if 'min_length' in rule and sent_len < rule['min_length']:
                    continue
                if 'max_length' in rule and sent_len > rule['max_length']:
                    continue
                # limitation by matching a regex
                if ('matches_regex' in rule and
                        not re.search(rule['matches_regex'], orig_resp, re.IGNORECASE)):
                    continue
                if ('not_matches_regex' in rule and
                        re.search(rule['not_matches_regex'], orig_resp, re.IGNORECASE)):
                    continue
                # select what to add
                to_add = random.choice(rule['add'])
                # process entities
                to_add = self._replace_entities(to_add, context + ' ' + response, entities)
                # apply rules
                if rule['type'] == 'prefix':
                    response = to_add + ' ' + response
                elif rule['type'] == 'suffix':
                    if not re.search(r'[!.;?,]\s*$', response):
                        response += '.'
                    response += ' ' + to_add
        # return postprocessed system response
        return response

    def postprocess_for_news(self, case, response, entities, add_pref=True, add_suf=True, context='', username=''):
        """Main function: postprocess the given system response based
        on the loaded rules, using information about the user question and named entities
        and a "case" tag (which is whatever you define in the rules file).

        @param case: a tag preselecting which rules may trigger
        @param response: the system response to postprocess
        @param question: the preceding user question
        @param entities: all named entities found in the user question, or a single entity \
            that should be replaced
        @param context: the user question (may be left blank)
        @return: the postprocessed response
        """
        sent_len = response.count(' ') + 1

        # apply all rules
        for rule in self.rules:
            # rule applies to current case (or all cases)
            if 'cases' not in rule or case in rule['cases']:
                # only apply the rule with a given probability
                if 'probability' in rule and random.random() > rule['probability']:
                    continue
                # length limitation: ignore sentences that do not comply
                if 'min_length' in rule and sent_len < rule['min_length']:
                    continue
                if 'max_length' in rule and sent_len > rule['max_length']:
                    continue
                # limitation by matching a regex
                if ('matches_regex' in rule and
                        not re.search(rule['matches_regex'], response, re.IGNORECASE)):
                    continue
                if ('not_matches_regex' in rule and
                        re.search(rule['not_matches_regex'], response, re.IGNORECASE)):
                    continue
                # select what to add
                to_add = random.choice(rule['add'])
                # process entities
                to_add = self._replace_entities(to_add, context + ' ' + response, entities)
                # apply rules
                if rule['type'] == 'prefix' and add_pref:
                    response = to_add + ' ' + response
                elif rule['type'] == 'suffix' and add_suf:
                    if not re.search(r'[!.;?,]\s*$', response):
                        response += '.'
                    response += ' ' + to_add
        # return postprocessed system response
        return response
