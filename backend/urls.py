#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.conf.urls import url

from backend import views

__author__ = 'Sheng Chen'

urlpatterns = [
    url(r'^stacks$', views.stack_list),
    url(r'^stacks/(?P<stack_name>(.*))/yml$', views.stack_yml),
    url(r'^clusters$', views.cluster_list),
    url(r'^clusters/(?P<cluster_name>(.*))$', views.cluster_detail),

]