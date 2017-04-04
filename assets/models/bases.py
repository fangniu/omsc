#!/usr/bin/env python
# _*_coding:utf-8_*_


from assets.models.auth import UserProfile
from django.db import models

__author__ = 'Sheng Chen'


class Asset(models.Model):
    Component = 0
    Server = 1
    Switcher = 2
    type_choices = (
        (Component, u'组件'),
        (Server, u'服务器'),
        (Switcher, u'交换机')
    )
    type = models.SmallIntegerField(choices=type_choices, max_length=64, default=Server, verbose_name=u'资产类型')
    manufacturer = models.ForeignKey('Manufacturer', verbose_name=u'制造商', null=True, blank=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
    trade_date = models.DateField(u'购买时间', null=True, blank=True)
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    price = models.FloatField(u'价格', null=True, blank=True)
    status_choices = ((0, u'在线'),
                      (1, u'已下线'),
                      (2, u'未知'),
                      (3, u'故障'),
                      (4, u'备用'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    memo = models.TextField(u'备注', null=True, blank=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = u'资产'
        verbose_name_plural = u"资产"

    def __str__(self):
        return '<type:%s id:%s>' % (self.type, self.id)


class IDC(models.Model):
    name = models.CharField(u'机房名称', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = u"机房"


class Tag(models.Model):
    name = models.CharField('Tag name', max_length=32, unique=True)
    create_by = models.ForeignKey('UserProfile')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    memo = models.TextField(u'备注', blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = u'合同'
        verbose_name_plural = u"合同"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'厂商'
        verbose_name_plural = u"厂商"