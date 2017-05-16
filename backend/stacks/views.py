#!/usr/bin/env python
# _*_coding:utf-8_*_

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from stacks import get_all_stacks, get_stack_yml, create_stack
from schema_validation import check_stack
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


@api_view(['GET'])
def stack_yml(request, stack_name):
    check_stack_exist(stack_name)
    yml = get_stack_yml(stack_name)
    return Response(rest(yml))


def check_stack_exist(stack_name):
    stacks = get_all_stacks()
    if stack_name not in stacks:
        raise Http404
