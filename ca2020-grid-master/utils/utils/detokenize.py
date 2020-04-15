#!/usr/bin/env python
# coding=utf-8


from __future__ import unicode_literals

from regex import Regex, UNICODE, IGNORECASE


class Detokenizer(object):
    """\
    A simple de-tokenizer class.
    """

    def __init__(self):
        """\
        Constructor (pre-compile all needed regexes).
        """
        # compile regexes
        self._currency_or_init_punct = Regex(r' ([\p{Sc}\(\[\{\¿\¡]+) ', flags=UNICODE)
        self._noprespace_punct = Regex(r' ([\,\.\?\!\:\;\\\%\}\]\)]+) ', flags=UNICODE)
        self._contract = Regex(r" (\p{Alpha}+) ' ?(ll|ve|re|[dsmt])(?= )", flags=UNICODE | IGNORECASE)
        self._fixes = Regex(r" (do|go[nt]|wan) (n't|ta|na)(?= )", flags=UNICODE | IGNORECASE)
        self._replace_table = {' i ': ' I ',
                               ' im ': ' I\'m ',
                               ' dont ': ' don\'t '}

    def detokenize(self, text):
        """\
        Detokenize the given text.
        """
        text = ' ' + text + ' '
        text = self._currency_or_init_punct.sub(r' \1', text)
        text = self._noprespace_punct.sub(r'\1 ', text)
        text = self._contract.sub(r" \1'\2", text)
        text = self._fixes.sub(r' \1\2', text)
        for tok, repl in self._replace_table.items():
            text = text.replace(tok, repl)
        text = text.strip()
        # capitalize
        if not text:
            return ''
        text = text[0].upper() + text[1:]
        return text
