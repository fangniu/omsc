#!/usr/bin/env python
# _*_coding:utf-8_*_

from salt.client import LocalClient

__author__ = 'Sheng Chen'


salt_client = LocalClient()


if __name__ == '__main__':
    print salt_client.cmd('*', 'test.ping')