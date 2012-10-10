# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2012 Mathias Weber <mathew.weber@gmail.com>
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
import json
import time
from threading import Thread

from snakebuild.resourceserver.resource import ResourceManager, \
        ResourceException
from test_helpers.versioneddir_helper import create_versioned_dir, \
        remove_versioned_dir


class TestResourceManager(unittest.TestCase):
    ''' The unit test for the snake build resourceserver resourcemanager
        class.
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

    def tearDown(self):
        ''' Clean up the directories '''
        remove_versioned_dir('resources')

    def test_resourcemanager_creation(self):
        ''' Test the resourcemanager creation
        '''
        with self.assertRaises(ResourceException):
            mgr = ResourceManager("/tmp/")

        mgr = ResourceManager(self.repo)
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
        mgr = ResourceManager(self.repo)
        self.assertTrue(len(mgr.resources) == 2)
        self.assertTrue(mgr.acquire('Arther', 'test1', False) == 'Test1')

    def test_release_command(self):
        ''' Test the release method if it uses the right resource.
        '''
        mgr = ResourceManager(self.repo)
        name = mgr.acquire('Arther', 'test1', False)
        self.assertTrue(name == 'Test1')
        self.assertTrue(mgr.release(name, 'Arther', False))

        # get more instances then available (must block)
        name = mgr.acquire('Arther', 'test1', False)
        self.assertTrue(name == 'Test1')
        name = mgr.acquire('Arther', 'test1', False)
        self.assertTrue(name == 'Test1')
        tobj = ThreadWaiter(mgr, 'test1', 'Arther', False)
        tobj.start()
        time.sleep(0.5)
        self.assertTrue(tobj.is_alive())
        self.assertTrue(mgr.release(name, 'Arther', False))
        tobj.join(0.5)
        self.assertFalse(tobj.is_alive())

        # still two instances acquired get an exclusive one now
        tobj = ThreadWaiter(mgr, 'test1', 'Arther', True)
        tobj.start()
        time.sleep(0.5)
        self.assertTrue(tobj.is_alive())
        self.assertTrue(mgr.release(name, 'Arther', False))
        self.assertTrue(tobj.is_alive())
        self.assertTrue(mgr.release(name, 'Arther', False))
        tobj.join(0.5)
        self.assertFalse(tobj.is_alive())
        self.assertTrue(mgr.release(name, 'Arther', False))

    def test_shutdown_command(self):
        ''' Test the shutdown command
        '''
        mgr = ResourceManager(self.repo)
        name = mgr.acquire('Arther', 'test1', False)
        self.assertTrue(name == 'Test1')
        name = mgr.acquire('Arther', 'test1', False)
        self.assertTrue(name == 'Test1')

        tobj = ThreadWaiter(mgr, 'test1', 'Arther', True)
        tobj.start()
        time.sleep(0.5)
        self.assertTrue(tobj.is_alive())
        self.assertTrue(mgr.release(name, 'Arther', False))
        self.assertTrue(tobj.is_alive())
        mgr.shutdown()
        tobj.join(0.5)
        self.assertFalse(tobj.is_alive())

    def test_loading_invalid_resources(self):
        ''' Test a repository with illegal resources. '''
        # create a custom versioned repos with three files
        # test1.resource (the same as in the one above)
        # .test2.resource (should not be loaded since a hidden file)
        # test2.resource.bkp (should not be loaded since bakup)
        repo = create_versioned_dir('iresources')

        data = {"name": "Test1",
                "parallel_count": 2,
                "keywords": ["myTest", "build", "build"],
                "parameters": {"value1": "arther"}}
        tfile = open(repo.get_local_path('test1.resource'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()
        repo.add('test1.resource')
        tfile = open(repo.get_local_path('test1_clone.resource'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()
        repo.add('test1_clone.resource')

        data = {"name": "Test2",
                "parallel_count": 4,
                "keywords": ["myTest", "build", "run"],
                "parameters": {"value1": "trillian"}}
        tfile = open(repo.get_local_path('.test2.resource'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()
        repo.add('.test2.resource')

        tfile = open(repo.get_local_path('test2.resource.bkp'), 'w')
        tfile.write(json.dumps(data))
        tfile.close()
        repo.add('test2.resource.bkp')

        repo.commit('Tester', 'test@snakebuild.org', 'added '
                'resourcemanager tests')
        repo.push_remote()

        # now test the resourcemanager initialisation
        mgr = ResourceManager(repo)
        self.assertTrue(len(mgr.resources) == 1)
        # test resources names
        self.assertTrue('Test1' in mgr.resources)
        self.assertTrue(mgr.resources['Test1'].name == 'Test1')

        # test keywords
        self.assertTrue('test1' in mgr.keywords)
        self.assertTrue('mytest' in mgr.keywords)
        self.assertTrue('build' in mgr.keywords)
        self.assertTrue(len(mgr.keywords) == 3)

        # clean up
        remove_versioned_dir('iresources')


class ThreadWaiter(Thread):
    ''' This is a helper class which tries to acquire a resource
        and waits till it gets the resource.
    '''
    def __init__(self, manager, resourcename, username, exclusive):
        ''' CTor
            @param manager: The resource manager to use
            @param resourcename: The resource name/tag to acquire
            @param username: The username to use for the acquire
            @param exclusive: Get the resource exclusive?
        '''
        Thread.__init__(self)
        self.manager = manager
        self.resourcename = resourcename
        self.username = username
        self.exclusive = exclusive

    def run(self):
        ''' Wait for the resource to be available for the exclusive job. '''
        self.manager.acquire(self.username, self.resourcename, self.exclusive)
