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
import json

from snakebuild.resourceserver.servercommands import COMMANDS
from snakebuild.resourceserver.servercmds import *
from snakebuild.communication.commandstructure import FUNCTION, SUCCESS, ERROR
from snakebuild.resourceserver.resource import ResourceManager
from test_helpers.versioneddir_helper import create_versioned_dir


class TestCommands(unittest.TestCase):
    ''' The unit test for the snake build resourceserver commands.
    '''
    def setUp(self):
        ''' Setup the test case. Create a directory for the test resources. If
            it allready exists remove it.
        '''
        self.repo = create_versioned_dir('resources')

        data = {"name": "Test1",
                "parallel_count": 2,
                "keywords": ["myTest", "build"],
                "parameters": {"value1": "arther"}}
        tfile = open(self.repo.get_local_path('test1.resource'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()
        self.repo.add('test1.resource')

        data = {"name": "Test2",
                "parallel_count": 4,
                "keywords": ["myTest", "build", "run"],
                "parameters": {"value1": "trillian"}}
        tfile = open(self.repo.get_local_path('test2.resource'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()
        self.repo.add('test2.resource')
        self.repo.commit('Tester', 'test@snakebuild.org', 'added '
                'resourcemanager tests')
        self.repo.push_remote()

    def test_status_list_cmd(self):
        ''' Test the status_list command.
        '''
        mgr = ResourceManager(self.repo)

        # test before any action
        result = COMMANDS['status_list'][FUNCTION](mgr)

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

        result = COMMANDS['status_list'][FUNCTION](mgr)

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

    def test_resource_details_cmd(self):
        ''' Test the resource_details command
        '''
        mgr = ResourceManager(self.repo)

        # test before any action
        result = COMMANDS['resource_details'][FUNCTION](mgr, 'Test1')

        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
        self.assertTrue('resource' in result)
        resource = result['resource']
        self.assertTrue(type(resource) == dict)
        self.assertTrue('name' in resource)
        self._checkresource(resource, 'Test1', ['test1', 'mytest', 'build'],
                    2, 2, [])
        self.assertTrue('parameters' in resource)
        self.assertTrue(type(resource['parameters']) == dict)
        self.assertTrue('value1' in resource['parameters'])
        self.assertTrue(resource['parameters']['value1'] == 'arther')

        # test with not existing resource
        result = COMMANDS['resource_details'][FUNCTION](mgr, 'Test11')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue('status' in result)
        self.assertTrue('message' in result)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

        # test with illegal parameter
        result = COMMANDS['resource_details'][FUNCTION](mgr, ['Test11'])
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue('status' in result)
        self.assertTrue('message' in result)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

    def test_acquire_release_cmds(self):
        ''' Test the acquire and the release functions of the resource server.
        '''
        mgr = ResourceManager(self.repo)

        result = COMMANDS['acquire'][FUNCTION](mgr, 'Pingg', 'Test1')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
        self.assertTrue('resource' in result)
        resource = result['resource']
        self.assertTrue(type(resource) == str or type(resource) == unicode)

        result = COMMANDS['release'][FUNCTION](mgr, 'Pingg', 'Test1')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
        self.assertTrue('resource' in result)
        resource = result['resource']
        self.assertTrue(type(resource) == str or type(resource) == unicode)
        # TODO add more tests here and check the status of the resources

        # not existing resource
        result = COMMANDS['acquire'][FUNCTION](mgr, 'Pingg', 'Test11')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

        # not existing resource
        result = COMMANDS['release'][FUNCTION](mgr, 'Pingg', 'Test11')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

        # not existing user
        result = COMMANDS['release'][FUNCTION](mgr, 'Pingu', 'Test1')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

        # not acquired
        result = COMMANDS['release'][FUNCTION](mgr, 'Pingg', 'Test1')
        self.assertTrue(len(result) == 2)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == ERROR)
        self.assertTrue(len(result['message']) > 0)

    def test_shutdown_cmd(self):
        ''' Test the private shutdown function. '''
        mgr = ResourceManager(self.repo)

        # test before any action
        result = COMMANDS['shutdown'][FUNCTION](mgr)

        self.assertTrue(len(result) == 1)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
        self.assertTrue(mgr.run == False)

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
