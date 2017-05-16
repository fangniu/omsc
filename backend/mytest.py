#!/usr/bin/env python
# _*_coding:utf-8_*_

from docker import DockerClient
import yaml

__author__ = 'Sheng Chen'

if __name__ == '__main__':

    # docker_client = DockerClient(base_url="10.0.2.5:2375")
    # print docker_client.containers.list()
    file_path = '/github/omsc/cs.yml'
    try:
        print yaml.load(file(file_path))
    except Exception, e:
        print type(e)

