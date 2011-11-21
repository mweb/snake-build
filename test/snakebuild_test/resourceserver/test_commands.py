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

from snakebuild.resourceserver.commands import COMMANDS
from snakebuild.communication.command_structure import FUNCTION
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
        result = COMMANDS['status_list'][FUNCTION]('status_list', None, mgr)

        # test result
        self.assertTrue(len(result) == 2)
