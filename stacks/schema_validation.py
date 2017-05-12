#!/usr/bin/env python
# _*_coding:utf-8_*_


from jsonschema import validate, FormatChecker
from stacks import get_all_stacks

__author__ = 'Sheng Chen'


stack_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "content": {"type": "string"},
    },
    "required": ["name", "content"],
    "additionalProperties": False
}


def check_stack(stack_info):
    try:
        validate(stack_info, stack_schema, format_checker=FormatChecker())
        if stack_info['name'] in get_all_stacks():
            return "Stack name conflict!"
    except Exception, e:
        return e.message