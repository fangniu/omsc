#!/usr/bin/env python
# _*_coding:utf-8_*_


import yaml
from yaml.scanner import ScannerError
from jsonschema import validate, FormatChecker
from projects import get_all_projects

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

cluster_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "address": {
            "oneOf": [
                    {"$ref": "#/definitions/swarm_tcp"},
                    {"$ref": "#/definitions/swarm_socket"}
                ],
        },
    },
    "definitions": {
        "swarm_tcp": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "format": "ipv4"
                },
                "port": {"type": "number"},
            },
            "required": ["ip", "port"],
            "additionalProperties": False
        },
        "swarm_socket":
            {
                "type": "object",
                "properties": {
                    "socket": {"type": "string"},
                },
                "required": ["socket"],
                "additionalProperties": False
            },

    },
    "required": ["name", "address"],
    "additionalProperties": False
}


def check_project(project_info):
    try:
        validate(project_info, stack_schema, format_checker=FormatChecker())
        if project_info['name'] in get_all_projects():
            return "Project name conflict!"
        content = yaml.load(project_info['content'])
        if type(content) != dict:
            return "FormatError: The field 'content' is invalid"
    except ScannerError:
        return "FormatError: The field 'content' is invalid"
    except Exception, e:
        print type(e)
        return e.message



def check_cluster(info):
    try:
        validate(info, cluster_schema, format_checker=FormatChecker())
    except Exception, e:
        return e.message
