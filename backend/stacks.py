#!/usr/bin/env python
# _*_coding:utf-8_*_

from omsc.conf import STACKS_DIR
import yaml
import os


__author__ = 'Sheng Chen'


def get_all_stacks():
    generator = os.walk(STACKS_DIR)
    _0, stacks_list, _2 = generator.next()
    return stacks_list


def create_stack(stack_info):
    stack_name = stack_info['name']
    stack_yml_str = stack_info['content']
    stack_dir = os.path.join(STACKS_DIR, stack_name)
    os.mkdir(stack_dir)
    stack_yml_path = os.path.join(stack_dir, 'docker-compose.yml')
    yaml.safe_dump(yaml.load(stack_yml_str), open(stack_yml_path, 'w'), default_flow_style=False, width=float("inf"))


def get_stack_yml(stack_name):
    stack_path = os.path.join(STACKS_DIR, stack_name, 'docker-compose.yml')
    if os.path.exists(stack_path):
        # return yaml.load(file(stack_path))
        with open(stack_path) as f:
            return f.read()




if __name__ == '__main__':
    print get_all_stacks()
