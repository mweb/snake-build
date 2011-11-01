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

from snakebuild.resourceserver.resource import Resource, \
        init_resource_from_string


class TestResource(unittest.TestCase):
    ''' The unit test for the snake build resourceserver resource class. '''
    def setUp(self):
        ''' Setup the test case. '''
        pass

    def test_resource_creation(self):
        ''' Test the resource creation methods.
        '''
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
        self.assertTrue(not res.release('unit_test', False))
        self.assertTrue(res.parallel_count == 4)
        self.assertTrue(res.current_count == 4)

        # test different user to release
        self.assertTrue(res.acquire('unit_test1', False, True))
        self.assertTrue(not res.release('unit_test', False))
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
        self.assertTrue(not res.release('unit_test', True))
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
