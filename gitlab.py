# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import requests

headers = {}
indent = 4


def encode(name):
    return name.replace('/', '%2F')


def project_members(project_name, indent_level):
    url = 'https://gitlab.com/api/v4/projects/{}/members'.format(encode(project_name))
    response = requests.get(url, headers=headers)

    for member in response.json():
        print(' ' * indent * indent_level, 'member -', member['id'], '-', member['username'])


def group_members(group_name, indent_level):
    url = 'https://gitlab.com/api/v4/groups/{}/members'.format(encode(group_name))
    response = requests.get(url, headers=headers)

    for member in response.json():
        print(' ' * indent * indent_level, 'member -', member['id'], '-', member['username'])


def group_projects(group_name, indent_level):
    url = 'https://gitlab.com/api/v4/groups/{}/projects'.format(encode(group_name))
    response = requests.get(url, headers=headers)

    for project in response.json():
        print(' ' * indent * indent_level, 'project -', project['id'], '-', project['name'], '-', project['visibility'])
        project_members(project['path_with_namespace'], indent_level + 1)


def navigate_subgroups(group_name, indent_level):
    group_members(group_name, indent_level)
    group_projects(group_name, indent_level)

    url = 'https://gitlab.com/api/v4/groups/{}/subgroups'.format(encode(group_name))
    response = requests.get(url, headers=headers)

    for subgroup in response.json():
        print(' ' * indent * indent_level, 'subgroup -', subgroup['id'], '-', subgroup['full_path'])
        navigate_subgroups(subgroup['full_path'], indent_level + 1)


if __name__ == '__main__':
    token = sys.argv[1]
    root_group = sys.argv[2]

    headers['Private-Token'] = token

    print('root group -', root_group)
    navigate_subgroups(root_group, 1)
