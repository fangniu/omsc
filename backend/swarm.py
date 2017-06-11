#!/usr/bin/env python
# _*_coding:utf-8_*_

from docker import DockerClient
from models import DockerSwarm
from utils import cache

__author__ = 'Sheng Chen'


@cache
def get_docker_client(cluster_name):
    cluster = DockerSwarm.objects.get(name=cluster_name)
    try:
        return DockerClient(base_url=cluster.base_url)
    except Exception:
        pass


if __name__ == '__main__':
    dc = DockerClient(base_url='unix://var/run/docker.sock')
    print dc.swarm.attrs