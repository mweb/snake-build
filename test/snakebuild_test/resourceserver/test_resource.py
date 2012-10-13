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
import time
from threading import Thread

from snakebuild.resourceserver.resource import init_resource_from_string, \
        init_resource_from_obj, ResourceException


class TestResource(unittest.TestCase):
    ''' The unit test for the snake build resourceserver resource class. '''
    def setUp(self):
        ''' Setup the test case. '''
        pass

    def test_resource_creation(self):
        ''' Test the resource creation methods.
        '''
        # from a json string
        demo = '''{ "name": "Test1",
                    "parallel_count" : 2,
                    "keywords": ["myTest", "build"],
                    "parameters": { "value1" : "arther" }
                  }
                '''

        res = init_resource_from_string(demo)
        self.assertTrue(res.name == "Test1")
        self.assertTrue(res.parallel_count == 2)
        self.assertTrue(res.current_count == 2)
        self.assertTrue('mytest' in res.keywords)
        self.assertTrue('build' in res.keywords)
        self.assertTrue('test1' in res.keywords)
        self.assertTrue(res.parameters['value1'] == 'arther')

        # from object now
        demo_obj = {'name': 'Test1',
                'parallel_count': 3,
                'keywords': ['myTest', 'build'],
                'parameters': {'value1': 'arther'}
                }

        res = init_resource_from_obj(demo_obj)
        self.assertTrue(res.name == "Test1")
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 3)
        self.assertTrue('mytest' in res.keywords)
        self.assertTrue('build' in res.keywords)
        self.assertTrue('test1' in res.keywords)
        self.assertTrue(res.parameters['value1'] == 'arther')

        # from a json string (incomplete)
        demo = '''{ "name": "Test1",
                    "keywords": ["myTest", "build"],
                    "parameters": { "value1" : "arther" }
                  }
                '''
        with self.assertRaises(ResourceException):
            res = init_resource_from_string(demo)

        # from object now (incomplete)
        demo_obj = {'name': 'Test1',
                'parallel_count': 3,
                'keywords': ['myTest', 'build'],
                }
        with self.assertRaises(ResourceException):
            res = init_resource_from_obj(demo_obj)

        demo_obj = {'name': 'Test1',
                'parallel_count': 3,
                'parameters': {'value1': 'arther'}
                }
        with self.assertRaises(ResourceException):
            res = init_resource_from_obj(demo_obj)

        demo_obj = {'parallel_count': 3,
                'keywords': ['myTest', 'build'],
                'parameters': {'value1': 'arther'}
                }
        with self.assertRaises(ResourceException):
            res = init_resource_from_obj(demo_obj)

        # from object now (illegal name)
        demo_obj = {'name': 123,
                'parallel_count': 3,
                'keywords': ['myTest', 'build'],
                'parameters': {'value1': 'arther'}
                }
        with self.assertRaises(ResourceException):
            res = init_resource_from_obj(demo_obj)

        # from object now (count as string)
        demo_obj = {'name': "Test1",
                'parallel_count': "3",
                'keywords': ['myTest', 'build'],
                'parameters': {'value1': 'arther'}
                }
        res = init_resource_from_obj(demo_obj)
        self.assertTrue(res.name == "Test1")
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 3)
        self.assertTrue('mytest' in res.keywords)
        self.assertTrue('build' in res.keywords)
        self.assertTrue('test1' in res.keywords)
        self.assertTrue(res.parameters['value1'] == 'arther')

        # from object now (count as string an not a number)
        demo_obj = {'name': "Test1",
                'parallel_count': "three",
                'keywords': ['myTest', 'build'],
                'parameters': {'value1': 'arther'}
                }
        with self.assertRaises(ResourceException):
            res = init_resource_from_obj(demo_obj)

        # from object now (paramerters not as a dictionary)
        demo_obj = {'name': "Test1",
                'parallel_count': 3,
                'keywords': ['myTest', 'build'],
                'parameters': ['value1', 'arther']
                }
        with self.assertRaises(ResourceException):
            res = init_resource_from_obj(demo_obj)

        # from object now (with a duplicate key name)
        demo_obj = {'name': "Test1",
                'parallel_count': 3,
                'keywords': ['build', 'test1', 'myTest', 'build'],
                'parameters': {'value1': 'arther'}
                }
        res = init_resource_from_obj(demo_obj)
        self.assertTrue(res.name == "Test1")
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 3)
        self.assertTrue('mytest' in res.keywords)
        self.assertTrue('build' in res.keywords)
        self.assertTrue('test1' in res.keywords)
        self.assertTrue(res.parameters['value1'] == 'arther')

    def test_acquire_command(self):
        ''' Test the acquire method if it sets the counters correctly.
        '''
        demo = '''{ "name": "Test",
                    "parallel_count" : 4,
                    "keywords": [],
                    "parameters": {}
                  }
                '''
        res = init_resource_from_string(demo)
        self.assertTrue(res.name == "Test")
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)
        self.assertTrue(res.acquire('unit_test', False, True))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 3)
        self.assertTrue(res.acquire('unit_test', False, True))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 2)
        self.assertTrue(res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 1)
        self.assertTrue(res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 0)
        self.assertTrue(not res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 0)

        # test a infinit resource
        res.parallel_count = 0
        self.assertTrue(res.parallel_count == 0)
        self.assertTrue(res.current_count == -4)
        for i in range(100):
            self.assertTrue(res.acquire('unit_test', False, False))
            self.assertTrue(res.current_count == (-5 - i))
        tobj = ThreadExclusiveWaiter(res, 'unit_test_ex')
        tobj.start()
        self.assertTrue(tobj.is_alive())
        # wait quickly to be sure that the new thread has asked for the
        # resource
        time.sleep(.1)
        self.assertFalse(res.acquire('unit_test', False, False))
        for i in range(104):
            self.assertTrue(res.release('unit_test', False))
            self.assertTrue(res.current_count == (-103 + i))
        tobj.join(1.0)
        self.assertFalse(tobj.is_alive())

    def test_release_command(self):
        ''' Test the release method if it sets the counters correctly.
        '''
        demo = '''{ "name": "Test",
                    "parallel_count" : 4,
                    "keywords": [],
                    "parameters": {}
                  }
                '''
        res = init_resource_from_string(demo)
        self.assertTrue(res.name == "Test")
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)
        self.assertTrue(res.acquire('unit_test', False, True))
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)
        with self.assertRaises(ResourceException):
            res.release('unit_test', False)
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)

        # test different user to release
        self.assertTrue(res.acquire('unit_test1', False, True))
        with self.assertRaises(ResourceException):
            res.release('unit_test', False)
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 3)
        self.assertTrue(res.release('unit_test1', False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)

        # exclusive lock
        self.assertTrue(res.acquire('unit_test', True, False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 0)
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)

        # exlusive unlock
        self.assertTrue(res.acquire('unit_test', True, False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 0)
        self.assertTrue(res.release('unit_test', True))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 3)
        with self.assertRaises(ResourceException):
            res.release('unit_test', True)
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 3)
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)

    def test_counter_change(self):
        ''' Test the change of the counter during run
        '''
        demo = '''{ "name": "Test",
                    "parallel_count" : 4,
                    "keywords": [],
                    "parameters": {}
                  }
                '''
        res = init_resource_from_string(demo)
        self.assertTrue(res.name == "Test")
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)
        res.parallel_count = 3
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 3)

        self.assertTrue(res.acquire('unit_test', False, True))
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 2)
        res.parallel_count = 2
        self.assertTrue(res.parallel_count == 2)
        self.assertTrue(res.current_count == 1)

        self.assertTrue(res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 2)
        self.assertTrue(res.current_count == 0)
        self.assertTrue(not res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 2)
        self.assertTrue(res.current_count == 0)

        res.parallel_count = 1
        self.assertTrue(res.parallel_count == 1)
        self.assertTrue(res.current_count == -1)
        self.assertTrue(not res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 1)
        self.assertTrue(res.current_count == -1)

        res.parallel_count = 5
        self.assertTrue(res.parallel_count == 5)
        self.assertTrue(res.current_count == 3)
        self.assertTrue(res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 5)
        self.assertTrue(res.current_count == 2)

        res.parallel_count = 1
        self.assertTrue(res.parallel_count == 1)
        self.assertTrue(res.current_count == -2)
        self.assertTrue(not res.acquire('unit_test', False, False))
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 1)
        self.assertTrue(res.current_count == -1)
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.current_count == 1)

        # set parallel count with an exclusive lock on
        res.parallel_count = 2
        self.assertTrue(res.parallel_count == 2)
        self.assertTrue(res.current_count == 2)
        self.assertTrue(res.acquire('unit_test', True, True))
        self.assertTrue(res.parallel_count == 2)
        self.assertTrue(res.current_count == 0)
        res.parallel_count = 3
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 0)
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 3)
        self.assertTrue(res.current_count == 3)

        # illegal value string
        with self.assertRaises(ResourceException):
            res.parallel_count = "Test"
        # illegal value float
        with self.assertRaises(ResourceException):
            res.parallel_count = 12.43
        # illegal value boolean
        with self.assertRaises(ResourceException):
            res.parallel_count = False
        # illegal value negative integer
        with self.assertRaises(ResourceException):
            res.parallel_count = -12

    def test_shutdown_command(self):
        ''' Test the shutdown command
        '''
        demo = '''{ "name": "Test",
                    "parallel_count" : 4,
                    "keywords": [],
                    "parameters": {}
                  }
                '''
        res = init_resource_from_string(demo)
        self.assertTrue(res.name == "Test")
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)
        self.assertTrue(res.acquire('unit_test', False, True))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 3)
        res.do_shutdown()
        self.assertTrue(not res.acquire('unit_test', False, True))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 3)
        self.assertTrue(res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)
        self.assertTrue(not res.acquire('unit_test', False, False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)


class ThreadExclusiveWaiter(Thread):
    ''' This is a helper class which tries to acquire a resource exclusivly
        and waits till it gets the resource.
    '''
    def __init__(self, resource, username):
        ''' CTor
            @param resource: The resource to acquire
            @param username: The username to use for the acquire
        '''
        Thread.__init__(self)
        self.resource = resource
        self.username = username

    def run(self):
        ''' Wait for the resource to be available for the exclusive job. '''
        self.resource.acquire('unit_test', True, True)
