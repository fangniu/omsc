#!/usr/bin/env python
# _*_coding:utf-8_*_

from models import DockerSwarm

__author__ = 'Sheng Chen'


def create_cluster(info):
    cluster_name = info['name']
    if DockerSwarm.objects.filter(name=cluster_name):
        return
    cluster = DockerSwarm(name=cluster_name)
    if 'socket' in info['address']:
        cluster.socket = info['address']['socket']
    else:
        ip, port = info['address']
        cluster.ip = ip
        cluster.port = port
    cluster.save()
    return cluster


