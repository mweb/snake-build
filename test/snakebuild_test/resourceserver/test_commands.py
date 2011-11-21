# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
#
# This file is part of Snake-Build.
#
# Snake-Build is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Snake-Build is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Snake-Build.  If not, see <http://www.gnu.org/licenses/>
''' The unit test for the resource server commands. '''

import unittest
import os
import shutil
import json

from snakebuild.resourceserver.commands import COMMANDS
from snakebuild.communication.commandstructure import FUNCTION, SUCCESS, ERROR
from snakebuild.resourceserver.resource import ResourceManager


class TestCommands(unittest.TestCase):
    ''' The unit test for the snake build resourceserver commands.
    '''
    def setUp(self):
        ''' Setup the test case. Create a directory for the test resources. If
            it allready exists remove it.
        '''
        self.config_dir = os.path.join(os.path.dirname(__file__), '..', '..',
                'data')
        if os.path.isdir(os.path.join(self.config_dir, 'resources')):
            shutil.rmtree(os.path.join(self.config_dir, 'resources'))
        os.makedirs(os.path.join(self.config_dir, 'resources'))
        data = {"name": "Test1",
                "parallel_count": 2,
                "keywords": ["myTest", "build"],
                "parameters": {"value1": "arther"}}
        tfile = open(os.path.join(self.config_dir, 'resources',
                'test1.resource'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()

        data = {"name": "Test2",
                "parallel_count": 4,
                "keywords": ["myTest", "build", "run"],
                "parameters": {"value1": "trillian"}}
        tfile = open(os.path.join(self.config_dir, 'resources',
                'test2.resource'), 'w')
        tfile.write(json.dumps(data))

    def test_status_list_cmd(self):
        ''' Test the status_list command function.
        '''
        mgr = ResourceManager(os.path.join(self.config_dir, 'resources'))

        # test before any action
        result = COMMANDS['status_list'][FUNCTION]('status_list', None, mgr)

        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
        self.assertTrue('resources' in result)
        resources = result['resources']
        for res in resources:
            self.assertTrue('name' in res)
            if res['name'] == 'Test1':
                self._checkresource(res, 'Test1', ['test1', 'mytest', 'build'],
                        2, 2, [])
            elif res['name'] == 'Test2':
                self._checkresource(res, 'Test2', ['test2', 'mytest', 'build',
                        'run'], 4, 4, [])

        # test after some actions
        mgr.acquire('Ford', 'test2', False)
        mgr.acquire('Beeblebrox', 'test2', False)
        mgr.acquire('Zaphod', 'test2', False)
        mgr.acquire('Ford', 'test1', True)

        result = COMMANDS['status_list'][FUNCTION]('status_list', None, mgr)

        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
        self.assertTrue('resources' in result)
        resources = result['resources']
        for res in resources:
            self.assertTrue('name' in res)
            if res['name'] == 'Test1':
                self._checkresource(res, 'Test1', ['test1', 'mytest', 'build'],
                        2, 0, ['Ford'])
            elif res['name'] == 'Test2':
                self._checkresource(res, 'Test2', ['test2', 'mytest', 'build',
                        'run'], 4, 1, ['Ford', 'Beeblebrox', 'Zaphod'])

        # test with wrong command name
        result = COMMANDS['status_list'][FUNCTION]('status', None, mgr)
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue('status' in result)
        self.assertTrue('message' in result)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

        # test with parameters
        result = COMMANDS['status_list'][FUNCTION]('status', {'action': 1},
                mgr)
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue('status' in result)
        self.assertTrue('message' in result)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

    def _checkresource(self, res, name, keywords, slots, free, users):
        ''' Check if the given resource full fills the following criteries.

            @param res: The resource to check
            @param name: The name of the resource
            @param keywords: The keywords this resource should have (a list)
            @param slots: The number of slots
            @param free: The number of free slots
            @param users: The current list with users
        '''
        self.assertTrue('keywords' in res)
        self.assertTrue('slots' in res)
        self.assertTrue('free'  in res)
        self.assertTrue('users' in res)
        self.assertTrue(res['name'] == name)
        for key in keywords:
            self.assertTrue(key in res['keywords'])
        self.assertTrue(len(keywords) == len(res['keywords']))
        self.assertTrue(res['slots'] == slots)
        self.assertTrue(res['free'] == free)
        for user in users:
            self.assertTrue(user in res['users'])
        self.assertTrue(len(users) == len(res['users']))