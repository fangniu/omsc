#!/usr/bin/env python
# _*_coding:utf-8_*_

import os

__author__ = 'Sheng Chen'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


VAR_DIR = os.path.join(BASE_DIR, 'var')

STACKS_DIR = os.path.join(VAR_DIR, 'stacks')


def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

create_dir_if_not_exists(VAR_DIR)

create_dir_if_not_exists(STACKS_DIR)