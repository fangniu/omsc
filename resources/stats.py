#!/usr/bin/env python
# _*_coding:utf-8_*_

from common.clients import salt_client
from common.exceptions import MinionConnectError

__author__ = 'Sheng Chen'


class HostStats(object):
    def __init__(self, minion_id):
        self.minion_id = minion_id
        if not salt_client.cmd(self.minion_id, 'test.ping'):
            raise MinionConnectError('ConnectError: %s ' % self.minion_id)

    @property
    def mem_available(self):
        return salt_client.cmd(self.minion_id, 'status.meminfo').get(self.minion_id).get('MemAvailable') / 1024

    @property
    def loadavg(self):
        return salt_client.cmd(self.minion_id, 'status.loadavg')

    @property
    def disk_usage(self):
        return salt_client.cmd(self.minion_id, 'disk.usage')

    @property
    def netdev(self):
        return salt_client.cmd(self.minion_id, 'status.netdev')



class ContainerStats(object):
    def __init__(self):
