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


class Stack(models.Model):
    version = models.CharField(max_length=8, default='3')
    name = models.CharField(max_length=255, unique=True)


    def __str__(self):
        return 'DockerStack:%s' % self.name


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    labels = models.TextField(null=True)
    stack = models.ForeignKey(
        Stack,
        on_delete=models.CASCADE,
        related_name='services',
        related_query_name='service'
    )
    # class Meta:
    #     unique_together = ('host', 'name')

    def __str__(self):
        return 'Service:%s' % self.name


class Volume(models.Model):
    mode_choices = (
        ('ro', 'read_only'),
        ('rw', 'read_write'),
        ('wo', 'write_only'),
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='volumes',
        related_query_name='volume'
    )
    host_path = models.CharField(max_length=255)
    container_path = models.CharField(max_length=255)
    mode = models.CharField(choices=mode_choices, max_length=8, default='rw')

    class Meta:
        unique_together = ('service', 'host_path')

    def __str__(self):
        return '%s->%s:%s' % (self.host_path, self.container_path, self.get_mode_display())


class Port(models.Model):
    host_port = models.IntegerField()
    service_port = models.IntegerField()
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='ports',
        related_query_name='port'
    )

    class Meta:
        unique_together = ('service', 'host_port')

    def __str__(self):
        return '%s->%s' % (self.host_port, self.service_port)


class Environment(models.Model):
    key = models.IntegerField()
    value = models.IntegerField()
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='environments',
        related_query_name='environment'
    )

    class Meta:
        unique_together = ('service', 'key')

    def __str__(self):
        return '%s=%s' % (self.key, self.value)


class HealthCheck(models.Model):
    service = models.OneToOneField(Service)
    test = models.TextField()
    interval = models.IntegerField()
    timeout = models.IntegerField()
    retries = models.SmallIntegerField()

    def __str__(self):
        return '%s:%s' % (self.service.name, self.test)


class Deploy(models.Model):
    service = models.OneToOneField(Service)
    is_replicated = models.BooleanField(default=True)
    replicas = models.SmallIntegerField(null=True)

    def __str__(self):
        if self.is_replicated:
            return '%s replicas:%s' % (self.service.name, self.replicas)
        else:
            return '%s global' % self.service.name


class Constraint(models.Model):
    NodeId = 0
    NodeHostName = 1
    NodeRole = 2
    NodeLabels = 3
    EngineLabels = 4
    type_choices = (
        (NodeId, "node.id"),
        (NodeHostName, "node.hostname"),
        (NodeRole, "node.role"),
        (NodeLabels, "node.labels"),
        (EngineLabels, "engine.labels"),
    )
    type = models.SmallIntegerField(choices=type_choices)
    is_equal = models.BooleanField(default=True)
    label_key = models.CharField(max_length=255, null=True)
    value = models.CharField(max_length=255)
    deploy = models.OneToOneField(Deploy)

    def __str__(self):
        key = "%s.%s" % (self.get_type_display(), self.label_key) if self.label_key else self.get_type_display()
        operator = "=" if self.is_equal else "!="
        return '%s%s%s' % (key, operator, self.value)


class UpdateConfig(models.Model):
    parallelism = models.SmallIntegerField(null=True)
    delay = models.IntegerField(null=True)
    failure_pause = models.BooleanField(default=True)
    monitor = models.IntegerField(null=True)
    max_failure_ratio = models.FloatField(null=True)
    deploy = models.OneToOneField(Deploy)

    def __str__(self):
        string = []
        if self.parallelism:
            string.append("parallelism=%s" % self.parallelism)
        if self.delay:
            string.append("delay=%ss" % self.delay)
        if self.monitor:
            string.append("monitor=%ss" % self.monitor)
        if self.parallelism:
            string.append("max_failure_ratio=%s" % self.max_failure_ratio)
        if self.failure_pause:
            string.append("failure_pause_action=pause")
        else:
            string.append("failure_pause_action=continue")
        return '%s:%s' % (self.deploy.service.name, ','.join(string))


class ResourceLimit(models.Model):
    deploy = models.OneToOneField(Deploy)
    cpus = models.FloatField(null=True)
    memory = models.IntegerField(null=True)

    def __str__(self):
        return 'cpus:%s, memory:%s' % (self.cpus, self.memory)


class ResourceReservations(models.Model):
    deploy = models.OneToOneField(Deploy)
    cpus = models.FloatField(null=True)
    memory = models.IntegerField(null=True)

    def __str__(self):
        return 'cpus:%s, memory:%s' % (self.cpus, self.memory)


class RestartPolicy(models.Model):
    delay = models.IntegerField(null=True)
    ConditionNone = 0
    ConditionOnFailure = 1
    ConditionAny = 2
    condition_type = (
        (ConditionNone, "none"),
        (ConditionOnFailure, "on-failure"),
        (ConditionNone, "any")
    )
    condition = models.SmallIntegerField(choices=condition_type, null=True)
    max_attempts = models.SmallIntegerField(null=True)
    window = models.IntegerField(null=True)
    labels = models.TextField(null=True)

    def __str__(self):
        return 'condition:%s' % self.get_condition_display()


if __name__ == '__main__':
    # from docker import DockerClient
    # client = DockerClient(base_url="10.0.2.5:2376")
    from compose.cli.main import TopLevelCommand
    top = TopLevelCommand('cs')
    print top.version()
