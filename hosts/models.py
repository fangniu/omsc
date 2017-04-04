#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.db import models

__author__ = 'Sheng Chen'


class Host(models.Model):
    processor = models.SmallIntegerField(u'逻辑核心数')
    memory = models.IntegerField(u'内存(MB)')
    memo = models.TextField(u'备注', null=True, blank=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u"主机"

    def __str__(self):
        return '<type:%s id:%s>' % (self.type, self.id)