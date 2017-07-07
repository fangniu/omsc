#!/usr/bin/env python
# _*_coding:utf-8_*_

import subprocess
from errors import DockerCliError

__author__ = 'Sheng Chen'


class Entry(object):
    def __init__(self, attrs_line):
        attrs = attrs_line.split()
        if len(attrs) == 9:
            self.uuid, self.name, self.image, self.node, self.desired_state, self.current_state, _1, _2, _3 = attrs
        else:
            self.uuid, self.name, self.image, self.node, self.desired_state, self.current_state, _1, _2, _3 = attrs[:9]
        self.current_state = " ".join([self.current_state, _1, _2, _3])

    @property
    def container_name(self):
        return self.name + '.' + self.uuid


class Service(object):
    def __init__(self, attrs_line):
        attrs = attrs_line.split()
        self.uuid, self.name, self.mode, self.replicas, self.image = attrs

    def rm(self):
        return execute(["docker", "service", "rm", self.name])

    def scale(self, replicas):
        return execute(["docker", "service", "scale", "%s=%s" % (self.name, replicas)])


class Stack(object):
    def __init__(self, name):
        self.name = name
        self.service_num = StackCli.ls().get(self.name)

    def get_entries(self, service_name=None):
        if service_name:
            return [Entry(line) for line in StackCli.ps(self.name, service_name)]
        return [Entry(line) for line in StackCli.ps(self.name)]

    @property
    def services(self):
        return StackCli.services(self.name)

    def ps_service(self, name):
        return self.services.get(name)

    def deploy(self, compose_file_path):
        sp = subprocess.Popen(["docker", "stack", "deploy", "-c", compose_file_path, self.name],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE
                              )
        sp.wait()
        if sp.returncode:
            raise DockerCliError(sp.stderr.read())
        else:
            return sp.stdout.read()


class StackCli(object):
    def __init__(self):
        pass

    @classmethod
    def ls(cls):
        out = execute(["docker", "stack", "ls"])
        ret = {}
        stack_list = out.splitlines()[1:]
        for stack in stack_list:
            stack_name, service_num = stack.split()
            ret[stack_name] = int(service_num)
        return ret

    @classmethod
    def ps(cls, stack_name, service_name=None):

        cmd = ["docker", "stack", "ps", stack_name]
        if service_name:
            cmd.extend(["--filter=name=%s" % service_name])
        out = execute(cmd)
        return out.splitlines()[1:]

    @classmethod
    def services(cls, stack_name):
        ret = {}
        out = execute(["docker", "stack", "services", stack_name])
        service_lines = out.splitlines()[1:]
        for service_line in service_lines:
            service = Service(service_line)
            ret[service.name] = service
        return ret


def execute(command_list):
    sp = subprocess.Popen(command_list,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE
                          )
    sp.wait()
    if sp.returncode:
        raise DockerCliError(sp.stderr.read())
    else:
        return sp.stdout.read()
