#!/usr/bin/env python
# _*_coding:utf-8_*_


from models import Service, Volume, Port, Environment, HealthCheck, Constraint, UpdateConfig, ResourceLimit,\
    ResourceReservations, RestartPolicy, Deploy

__author__ = 'Sheng Chen'


def create_service(service_config):
    service_dict = {}
    service = Service(
        name=service_config['name'],
        image=service_config['image'],

    )


    deploy = Deploy(

    )



    if service_config.get('placement') and service_config['placement']['constraints']:
        constraint = Constraint(
            type=service_config['placement']['constraints']['type'],
            is_equal=service_config['placement']['constraints']['is_equal'],
            label_key=service_config['placement']['constraints'].get('label_key'),
            value=service_config['placement']['constraints']['value'],
        )
