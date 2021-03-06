#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from docker.errors import APIError
from stacks import Stack
from models import DockerSwarm
from errors import DockerCliError
from clusters import create_cluster
from swarm import get_docker_client
from schema_validation import check_new_project, check_project_yml, check_cluster
from projects import get_all_projects, get_project_yml, create_project, update_project, remove_project
from omsc.conf import STACKS_DIR
import os

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


@api_view(['GET', 'PUT', 'POST'])
def project_list(request):
    if request.method == 'GET':
        projects = get_all_projects()
        return Response(rest(projects))
    elif request.method == 'POST':
        ret = check_new_project(request.data)
        if ret:
            return Response(rest(message=ret, code=1))
        else:
            if project_exists(request.data['name']):
                return Response(rest(message="Project Conflict!", code=1))
            create_project(request.data)
            return Response(rest())


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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def project_yml(request, project_name):
    if not project_exists(project_name):
        raise Http404
    if request.method == 'GET':
        yml = get_project_yml(project_name)
        return Response(rest({'yaml': yml}))
    elif request.method == 'DELETE':
        remove_project(project_name)
        return Response(rest())
    elif request.method == 'PUT':
        content = request.data.get('yaml')
        if content:
            ret = check_project_yml(content, project_name)
            if ret:
                return Response(rest(message=ret, code=1))
            else:
                update_project(project_name, content)
                return Response(rest())
        else:
            return Response(rest(message="This field 'yaml' is required!"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def project(request, project_name):
    project_path = get_project_path(project_name)
    if not os.path.exists(project_path):
        raise Http404
    if request.method == 'POST':
        stack = Stack(project_name)
        try:
            out = stack.deploy(os.path.join(project_path, 'docker-compose.yml'))
            return Response(rest(message=out))
        except DockerCliError, e:
            return Response(rest(message=e.message, code=1))
    else:
        return Response(rest(message='TODO'), status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def service_remove(request, project_name, service_name):
    if not project_exists(project_name):
        raise Http404
    stack = Stack(project_name)
    service = stack.services.get(service_name)
    if service:
        try:
            out = service.rm()
            return Response(rest(message=out))
        except DockerCliError, e:
            return Response(rest(message=e.message, code=1))
    else:
        return Response(rest(message='No such service: %s' % service_name), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def service_scale(request, project_name, service_name):
    if not project_exists(project_name):
        raise Http404
    stack = Stack(project_name)
    service = stack.services.get(service_name)
    replicas = request.data.get("replicas")
    if not replicas:
        return Response(rest(message="This field 'replicas' is required!"), status=status.HTTP_400_BAD_REQUEST)
    if service:
        try:
            out = service.scale(int(replicas))
            return Response(rest(message=out))
        except DockerCliError, e:
            return Response(rest(message=e.message, code=1))
        except ValueError:
            return Response(rest(message="Invalid replicas"), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(rest(message='No such service: %s' % service_name), status=status.HTTP_400_BAD_REQUEST)


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


def project_exists(project_name):
    if os.path.exists(get_project_path(project_name)):
        return True


def get_project_path(project_name):
    return os.path.join(STACKS_DIR, project_name)