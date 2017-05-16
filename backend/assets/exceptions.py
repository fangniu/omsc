#!/usr/bin/env python
# _*_coding:utf-8_*_


__author__ = 'Sheng Chen'


class MinionConnectError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message