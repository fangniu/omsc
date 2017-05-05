#!/usr/bin/env python
# _*_coding:utf-8_*_

from omsc.settings import STACKS_DIR
from compose.config.validation import
import os

__author__ = 'Sheng Chen'


def get_stacks():
    ret = os.walk(STACKS_DIR).next()
    return ret[0], ret[2]



if __name__ == '__main__':
    print get_stacks()
