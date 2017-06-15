#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from docker.errors import APIError
from models import DockerSwarm
from clusters import create_cluster
from swarm import get_docker_client
from schema_validation import check_stack, check_cluster
from stacks import get_all_stacks, get_stack_yml, create_stack


__author__ = 'Sheng Chen'


def rest(body=None, message="", code=0):
    if code and message:
        pass
    elif code:
        message = 'Failed'
    elif message:
        pass
    else:
        message = 'Success'
    if body is None:
        body = dict()
    elif type(body) == list:
        body = {
            'items': body
        }
    return {
        'code': code,
        'message': message,
        'body': body
    }


@api_view(['GET', 'POST'])
def stack_list(request):
    if request.method == 'GET':
        stacks = get_all_stacks()
        return Response(rest(stacks))
    elif request.method == 'POST':
        ret = check_stack(request.data)
        if ret:
            return Response(rest(message=ret, code=1), status=status.HTTP_400_BAD_REQUEST)
        else:
            create_stack(request.data)
            return Response(rest(), status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def cluster_list(request):
    if request.method == 'GET':
        return Response(rest([s.to_json() for s in DockerSwarm.objects.all()]))
    elif request.method == 'POST':
        ret = check_cluster(request.data)
        if ret:
            return Response(rest(message=ret, code=1), status=status.HTTP_400_BAD_REQUEST)
        cluster = create_cluster(request.data)
        if cluster:
            return Response(rest())
        return Response(rest(message='cluster name conflict!', code=1), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def cluster_detail(request, cluster_name):
    if request.method == 'GET':
        cluster = get_cluster(cluster_name)
        if cluster:
            dc = get_docker_client(cluster_name)
            if dc:
                return Response(rest(dc.swarm.attrs))
            return Response(rest(message='connection error: %s' % cluster.base_url , code=1))
    elif request.method == 'POST':
        return Response(rest())


@api_view(['GET', 'POST'])
def node_list(request, cluster_name):
    if request.method == 'GET':
        cluster = get_cluster(cluster_name)
        if cluster:
            dc = get_docker_client(cluster_name)
            if dc:
                return Response(rest([n.attrs for n in dc.nodes.list()]))
            return Response(rest(message='connection error: %s' % cluster.base_url , code=1))
    elif request.method == 'POST':
        return Response(rest())


@api_view(['GET', 'POST'])
def node_detail(request, cluster_name, node_id):
    if request.method == 'GET':
        cluster = get_cluster(cluster_name)
        if cluster:
            dc = get_docker_client(cluster_name)
            if dc:
                return Response(rest(get_node(dc, node_id)))
            return Response(rest(message='connection error: %s' % cluster.base_url , code=1))
    elif request.method == 'POST':
        return Response(rest())


@api_view(['GET'])
def stack_yml(request, stack_name):
    check_stack_exist(stack_name)
    yml = get_stack_yml(stack_name)
    return Response(rest({'yaml': yml}))


def check_stack_exist(stack_name):
    stacks = get_all_stacks()
    if stack_name not in stacks:
        raise Http404


def get_cluster(cluster_name):
    try:
        return DockerSwarm.objects.get(name=cluster_name)
    except DockerSwarm.DoesNotExist:
        raise Http404


def get_node(docker_client, node_id):
    try:
        return docker_client.nodes.get(node_id).attrs
    except APIError:
        raise Http404