#!/usr/bin/env python
# _*_coding:utf-8_*_

from functools import wraps

__author__ = 'Sheng Chen'


def cache(func):
    caches = {}

    @wraps(func)
    def wrap(*args):
        if args not in caches:
            caches[args] = func(*args)
        return caches[args]
    return wrap