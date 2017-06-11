#!/usr/bin/env python
# _*_coding:utf-8_*_

# from compose.config.validation import
from omsc.conf import STACKS_DIR
import logging
import os
from os.path import normpath
from compose.container import Container
from compose.cli.command import get_project as compose_get_project, get_config_path_from_options, get_config_from_options
from compose.config.environment import Environment

from compose.cli.docker_client import docker_client
from compose.const import API_VERSIONS, COMPOSEFILE_V3_0

__author__ = 'Sheng Chen'


def get_project(stack_name):
    """
    get docker project given file path
    """
    stack_dir = os.path.join(STACKS_DIR, stack_name)

    logging.debug('get stack ' + stack_dir)

    environment = Environment.from_env_file(stack_dir)
    config_path = get_config_path_from_options(stack_dir, dict(), environment)
    project = compose_get_project(stack_dir, config_path)
    return project


def ps_(project):
    """
    containers status
    """
    logging.info('ps ' + project.name)
    running_containers = project.containers(stopped=True)

    items = [{
        'name': container.name,
        'name_without_project': container.name_without_project,
        'command': container.human_readable_command,
        'state': container.human_readable_state,
        'labels': container.labels,
        'ports': container.ports,
        'volumes': get_volumes(get_container_from_id(project.client, container.id)),
        'is_running': container.is_running} for container in running_containers]

    return items


def get_container_from_id(my_docker_client, container_id):
    """
    return the docker container from a given id
    """
    return Container.from_id(my_docker_client, container_id)


def get_volumes(container):
    """
    retrieve container volumes details
    """
    mounts = container.get('Mounts')
    return [dict(source=mount['Source'], destination=mount['Destination']) for mount in mounts]


def containers():
    """
    active containers
    """
    return client().containers()


def info():
    """
    docker info
    """
    docker_info = client().info()
    return dict(info=docker_info['ServerVersion'], name=docker_info['Name'])


def client():
    """
    docker client
    """
    return docker_client(Environment(), API_VERSIONS[COMPOSEFILE_V3_0])


def project_config(path):
    """
    docker-compose config
    """
    norm_path = normpath(path)
    return get_config_from_options(norm_path, dict())


if __name__ == '__main__':
    print get_project('/github/omsc/var/stacks/voting_app')
