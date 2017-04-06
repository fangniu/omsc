#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.db import models

__author__ = 'Sheng Chen'


class Host(models.Model):
    kernel = models.CharField(u'系统内核', max_length=32)
    cpu_model = models.CharField(u'CPU型号', max_length=255)
    num_cpus = models.SmallIntegerField(u'CPU核数')
    cpuarch = models.CharField(u'CPU架构', max_length=64)
    mem_total = models.IntegerField(u'内存(MB)')

    os = models.CharField(u'系统类型', max_length=128)
    os_release = models.CharField(u'系统版本', max_length=128)

    hostname = models.CharField(u'主机名', max_length=128)
    ip = models.GenericIPAddressField()
    fqdn = models.CharField("FQDN", max_length=255)
    memo = models.TextField(u'备注', null=True, blank=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u"主机"

    def __str__(self):
        return '<%s ip:%s>' % (self.hostname, self.ip)

