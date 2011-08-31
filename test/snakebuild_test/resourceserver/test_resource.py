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
    ''' The unit test for the snake build common Config class. '''
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

