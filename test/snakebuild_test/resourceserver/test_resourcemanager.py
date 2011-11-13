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
''' The unit test for the resource object '''

import unittest
import os
import shutil
import json

from snakebuild.resourceserver.resource import ResourceManager


class TestResourceManager(unittest.TestCase):
    ''' The unit test for the snake build resourceserver resourcemanager
        class.
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

    def test_resourcemanager_creation(self):
        ''' Test the resourcemanager creation
        '''
        mgr = ResourceManager(os.path.join(self.config_dir, 'resources'))
        self.assertTrue(len(mgr.resources) == 2)
        # test resources names
        self.assertTrue('Test2' in mgr.resources)
        self.assertTrue(mgr.resources['Test2'].name == 'Test2')
        self.assertTrue('Test1' in mgr.resources)
        self.assertTrue(mgr.resources['Test1'].name == 'Test1')

        # test keywords
        self.assertTrue('test1' in mgr.keywords)
        self.assertTrue('test2' in mgr.keywords)
        self.assertTrue('mytest' in mgr.keywords)
        self.assertTrue('build' in mgr.keywords)
        self.assertTrue('run' in mgr.keywords)

        # check resource if loaded correctly.
        self.assertTrue(mgr.resources['Test1'].parallel_count == 2)
        self.assertTrue('mytest' in mgr.resources['Test1'].keywords)
        self.assertTrue('build' in mgr.resources['Test1'].keywords)
        self.assertTrue('test1' in mgr.resources['Test1'].keywords)
        self.assertTrue('value1' in mgr.resources['Test1'].parameters)
        self.assertTrue(mgr.resources['Test1'].parameters['value1'] ==
                'arther')

        self.assertTrue(mgr.resources['Test2'].parallel_count == 4)
        self.assertTrue('mytest' in mgr.resources['Test2'].keywords)
        self.assertTrue('build' in mgr.resources['Test2'].keywords)
        self.assertTrue('run' in mgr.resources['Test2'].keywords)
        self.assertTrue('test2' in mgr.resources['Test2'].keywords)
        self.assertTrue(not 'test1' in mgr.resources['Test2'].keywords)
        self.assertTrue('value1' in mgr.resources['Test2'].parameters)
        self.assertTrue(mgr.resources['Test2'].parameters['value1'] ==
                'trillian')

    def test_acquire_command(self):
        ''' Test the acquire method if it sets the counters correctly.
        '''
        mgr = ResourceManager(os.path.join(self.config_dir, 'resources'))
        self.assertTrue(len(mgr.resources) == 2)
        self.assertTrue(mgr.acquire('Arther', 'test1', False) == 'Test1')

    def test_release_command(self):
        ''' Test the release method if it uses the right resource.
        '''
        mgr = ResourceManager(os.path.join(self.config_dir, 'resources'))
        name = mgr.acquire('Arther', 'test1', False)
        self.assertTrue(mgr.release(name, 'Arther', False))

    def test_shutdown_command(self):
        ''' Test the shutdown command
        '''
        pass