#!/usr/bin/env python
# _*_coding:utf-8_*_


import os
from yaml.scanner import ScannerError
from jsonschema import validate, FormatChecker
from projects import get_all_projects
from compose.cli.command import get_project
from compose.config.errors import ConfigurationError
from tempfile import NamedTemporaryFile

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


def check_new_project(project_info):
    try:
        validate(project_info, stack_schema, format_checker=FormatChecker())
        name = project_info['name']
        if name in get_all_projects():
            return "Project name conflict!"
        return check_project_yml(project_info['content'], name)
    except Exception, e:
        return e.message


def check_project_yml(project_yml, project_name=''):
    tmp_f = NamedTemporaryFile()
    try:
        tmp_f.write(project_yml)
        tmp_f.seek(0)
        get_project(os.path.dirname(tmp_f.name), config_path=[os.path.basename(tmp_f.name)])
    except ScannerError:
        return "FormatError: The field 'content' is invalid"
    except ConfigurationError, e:
        msg = str(e).replace(tmp_f.name, project_name)
        return msg
    finally:
        tmp_f.close()


def check_cluster(info):
    try:
        validate(info, cluster_schema, format_checker=FormatChecker())
    except Exception, e:
        return e.message
