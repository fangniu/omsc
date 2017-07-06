#!/usr/bin/env python
# _*_coding:utf-8_*_

from omsc.conf import STACKS_DIR
from composes import get_project
from compose.config.errors import ComposeFileNotFound
from stacks import Stack, StackCli
import yaml
import os
import shutil


__author__ = 'Sheng Chen'


def get_all_projects():
    ret = []
    generator = os.walk(STACKS_DIR)
    _0, projects_list, _2 = generator.next()
    try:
        for name in projects_list:
            project = get_project(name)
            stack = Stack(name)
            service_list = []
            for project_s in project.services:
                service = stack.ps_service(name + '_' + project_s.name)
                if service:
                    service_list.append({
                        "displayName": project_s.name,
                        "uuid": service.uuid,
                        "serviceName": service.name,
                        "mode": service.mode,
                        "replicas": service.replicas,
                        "image": service.image
                    })
                else:
                    service_list.append({
                        "displayName": project_s.name,
                    })
            ret.append({
                "name": name,
                "services": service_list,
                "state": "deployed" if name in StackCli.ls() else "undeployed"
            })
    except ComposeFileNotFound:
        pass
    return ret


def create_project(project_info):
    project_name = project_info['name']
    project_yml_str = project_info['content']
    stack_dir = os.path.join(STACKS_DIR, project_name)
    os.mkdir(stack_dir)
    stack_yml_path = os.path.join(stack_dir, 'docker-compose.yml')
    yaml.safe_dump(yaml.load(project_yml_str), open(stack_yml_path, 'w'), default_flow_style=False, width=float("inf"))


def update_project(project_name, project_yml_str):
    stack_yml_path = os.path.join(STACKS_DIR, project_name, 'docker-compose.yml')
    yaml.safe_dump(yaml.load(project_yml_str), open(stack_yml_path, 'w'), default_flow_style=False, width=float("inf"))


def remove_project(project_name):
    shutil.rmtree(os.path.join(STACKS_DIR, project_name))


def get_project_yml(project_name):
    project_path = os.path.join(STACKS_DIR, project_name, 'docker-compose.yml')
    if os.path.exists(project_path):
        # return yaml.load(file(stack_path))
        with open(project_path) as f:
            return f.read()


if __name__ == '__main__':
    print get_all_projects()
