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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u"主机"

    def __str__(self):
        return '<%s ip:%s>' % (self.hostname, self.ip)


class Container(models.Model):
    name = models.CharField(max_length=255, unique=True)
    hostname = models.CharField(max_length=255, unique=True)
    host = models.ForeignKey(
        Host,
        on_delete=models.CASCADE,
        related_name='containers',
        related_query_name='container'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255)

    class Meta:
        unique_together = ('host', 'name')

    def __str__(self):
        return 'Container:%s' % self.name


class Volume(models.Model):
    mode_choices = (
        ('ro', 'read_only'),
        ('rw', 'read_write'),
        ('wo', 'write_only'),
    )
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
        related_name='volumes',
        related_query_name='volume'
    )
    host_path = models.CharField(max_length=255)
    container_path = models.CharField(max_length=255)
    mode = models.CharField(choices=mode_choices, max_length=8, default='rw')

    class Meta:
        unique_together = ('container', 'host_path')

    def __str__(self):
        return '%s->%s:%s' % (self.host_path, self.container_path, self.get_mode_display())


class Port(models.Model):
    host_port = models.IntegerField()
    container_port = models.IntegerField()
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
        related_name='ports',
        related_query_name='port'
    )

    class Meta:
        unique_together = ('container', 'host_port')

    def __str__(self):
        return '%s->%s' % (self.host_port, self.container_port)


class Environment(models.Model):
    key = models.IntegerField()
    value = models.IntegerField()
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
        related_name='environments',
        related_query_name='environment'
    )

    class Meta:
        unique_together = ('container', 'key')

    def __str__(self):
        return '%s=%s' % (self.key, self.value)

if __name__ == '__main__':
    # from docker import DockerClient
    # client = DockerClient(base_url="10.0.2.5:2376")
    from compose.cli.main import TopLevelCommand
    top = TopLevelCommand('cs')
    print top.version()
