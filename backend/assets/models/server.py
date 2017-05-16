#!/usr/bin/env python
# _*_coding:utf-8_*_


from django.db import models
from bases import Asset

__author__ = 'Sheng Chen'


class Server(models.Model):
    asset = models.OneToOneField('Asset')
    PcServer = 0
    BladeServer = 1
    Rack = 2
    CreatedByAuto = 0
    CreatedByManual = 1
    sn = models.CharField(u'服务器SN号', max_length=128, unique=True)
    type_choices = (
        (PcServer, u'PC服务器'),
        (BladeServer, u'刀片机'),
        (Rack, u'Rack'),
    )
    created_by_choices = (
        (CreatedByAuto, 'Auto'),
        (CreatedByManual, 'Manual'),
    )
    type = models.SmallIntegerField(choices=type_choices, verbose_name=u"服务器类型", default=0)
    created_by = models.SmallIntegerField(choices=created_by_choices, default=CreatedByAuto)  # auto: auto created,   manual:created manually
    raid_type = models.CharField(u'raid类型', max_length=512, blank=True, null=True)

    host_name = models.CharField(u'主机名', max_length=255, blank=True, null=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = u"服务器"
        # together = ["sn", "asset"]

    def __str__(self):
        return '%s sn:%s' % (self.asset.type, self.sn)


class CPU(models.Model):
    server = models.ForeignKey('Server')
    model = models.CharField(u'型号', max_length=128)
    arch = models.CharField(u'架构', max_length=16)
    cpu_cores = models.SmallIntegerField(u'cpu核数')
    siblings = models.SmallIntegerField(u'每个core的逻辑核心数')
    processor = models.SmallIntegerField(u'逻辑核心数')
    memo = models.TextField(u'备注', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = u'CPU部件'
        verbose_name_plural = u"CPU部件"
        # unique_together = ("server", "model", "arch", "cpu_cores", "siblings", "processor")

    def __str__(self):
        return '%s:%s:%s' % (self.server.id, self.model, self.arch)


class RAM(models.Model):
    server = models.ForeignKey('Server')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s:%s:%s' % (self.server.id, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("server", "slot")


class Disk(models.Model):
    server = models.ForeignKey('Server')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    # manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ("server", "slot")
        verbose_name = u'硬盘'
        verbose_name_plural = u"硬盘"

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.server.id, self.slot, self.capacity)


class NIC(models.Model):
    server = models.ForeignKey('Server')
    name = models.CharField(u'网卡名', max_length=64, null=True)
    sn = models.CharField(u'SN号', max_length=128, null=True)
    model = models.CharField(u'网卡型号', max_length=128, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return '%s:%s' % (self.model, self.sn)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"
        # unique_together = ("asset_id", "slot")
        unique_together = ("server", "sn")


class RaidAdaptor(models.Model):
    server = models.ForeignKey('Server')
    sn = models.CharField(u'SN号', max_length=128, null=True)
    slot = models.CharField(u'插口', max_length=64)
    model = models.CharField(u'型号', max_length=64, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return '%s:%s:%s' % (self.server.id, self.slot, self.sn)

    class Meta:
        unique_together = ("server", "slot")
