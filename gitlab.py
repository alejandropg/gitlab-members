# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import requests

INDENT = 4

headers = {}
users = {}

# API documentation
# https://docs.gitlab.com/ee/api/api_resources.html#group-resources


class PageIterator:
    def __init__(self, url, headers):
        self._url = url
        self._headers = headers
        self._page = []
        self._index = 0
        self._has_next = None

    def hasNext(self):
        if self._index == len(self._page):
            self._get_next_page()
        return self._has_next

    def next(self):
        element = self._page[self._index]
        self._index += 1
        return element

    def _get_next_page(self):
        if self._url is None:
            self._has_next = False
            return

        response = self._http_get(self._url, self._headers)
        
        self._page = response.json()
        self._index = 0
        self._has_next = len(self._page) > 0
        self._url = self._locate_next_page_url(response)

    def _http_get(self, url, headers):
        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            print('ERROR ' + str(response.status_code) + ' when GET ' + url)
            print(reponse.text)
            reponse.raise_for_status()
        
        return response

    def _locate_next_page_url(self, response):
        linksStr = response.headers['link']
        # string format: <url> ; rel="xxx", <url> ; rel="xxx", ...

        url = None
        for element in linksStr.split(','):
            link = element.strip()
            if (link.endswith('rel="next"')):
                next_link_url = link.split(';')[0].strip()
                next_link_url_len = len(next_link_url)

                # Remove < > characters at the beginning and end of the url
                url = next_link_url[1:next_link_url_len-1]
                break

        return url


def encode(name):
    return name.replace('/', '%2F')

def project_members(project_name, indent_level):
    url = 'https://gitlab.com/api/v4/projects/{}/members'.format(encode(project_name))
    iterator = PageIterator(url, headers)
    iterator.hasNext()
    while iterator.hasNext():
        member = iterator.next()
        users[member['id']] = member['username']
        print(' ' * INDENT * indent_level, 'member -', member['id'], '-', member['username'])

def group_members(group_name, indent_level):
    url = 'https://gitlab.com/api/v4/groups/{}/members'.format(encode(group_name))
    iterator = PageIterator(url, headers)
    iterator.hasNext()
    while iterator.hasNext():
        member = iterator.next()
        users[member['id']] = member['username']
        print(' ' * INDENT * indent_level, 'member -', member['id'], '-', member['username'])

def group_projects(group_name, indent_level):
    url = 'https://gitlab.com/api/v4/groups/{}/projects'.format(encode(group_name))
    iterator = PageIterator(url, headers)
    iterator.hasNext()
    while iterator.hasNext():
        project = iterator.next()
        print(' ' * INDENT * indent_level, 'project -', project['id'], '-', project['name'], '-', project['visibility'])
        project_members(project['path_with_namespace'], indent_level + 1)


def navigate_subgroups(group_name, indent_level):
    group_members(group_name, indent_level)
    group_projects(group_name, indent_level)

    url = 'https://gitlab.com/api/v4/groups/{}/subgroups'.format(encode(group_name))
    iterator = PageIterator(url, headers)
    iterator.hasNext()
    while iterator.hasNext():
        subgroup = iterator.next()
        print(' ' * INDENT * indent_level, 'subgroup -', subgroup['id'], '-', subgroup['full_path'])
        navigate_subgroups(subgroup['full_path'], indent_level + 1)

if __name__ == '__main__':
    token = sys.argv[1]
    root_group = sys.argv[2]

    headers['Private-Token'] = token

    print('root group -', root_group)
    navigate_subgroups(root_group, 1)

    print()
    print()
    print('users:')
    sortedByName = sorted(users.items(), key=lambda kv: kv[1])
    for user_id, user_name in sortedByName:
        print(' ' * INDENT, str(user_id), '\t:', user_name)
