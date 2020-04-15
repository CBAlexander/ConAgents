#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def remove_dups_keep_order(seq):
    """Remove duplicates from a list while preserving order."""
    # http://stackoverflow.com/questions/480214
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
