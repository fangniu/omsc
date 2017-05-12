#!/usr/bin/env python
# _*_coding:utf-8_*_

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from stacks import get_all_stacks


__author__ = 'Sheng Chen'


# class StackListSerializer(serializers.Serializer):
#     name = serializers.CharField()
#
#     def create(self, validated_data):
#         pass


    # def to_representation(self, instance):
    #     compose_obj = Compose.get(id=instance.id)
    #     deployment_name = Deployment.get(id=compose_obj.deploymentId).name
    #     return {
    #         'deploymentName': deployment_name,
    #         'composeFileName': compose_obj.composeFileName
    #     }
