#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.conf.urls import url

from backend import views

__author__ = 'Sheng Chen'

urlpatterns = [
    url(r'^projects/(?P<project_name>(.*))/yml$', views.project_yml),
    url(r'^projects$', views.project_list),
    url(r'^clusters/(?P<cluster_name>(.*))/nodes/(?P<node_id>(.*))$', views.node_detail),
    url(r'^clusters/(?P<cluster_name>(.*))/nodes$', views.node_list),
    url(r'^clusters/(?P<cluster_name>(.*))$', views.cluster_detail),
    url(r'^clusters$', views.cluster_list),

]