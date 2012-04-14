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

from snakebuild.communication.server import REMOTE_COMMANDS
# this needs to be imported to fill the REMOTE_COMMANDS
import snakebuild.buildagent.agentcmds
from snakebuild.communication.commandstructure import FUNCTION, SUCCESS, ERROR


class TestCommands(unittest.TestCase):
    ''' The unit test for the snake build build agent commands.
    '''
    def setUp(self):
        ''' Setup the test case.
        '''
        pass

    def test_status_list_cmd(self):
        ''' Test the status_list command.
        '''
#        agent = BuildAgent()
        agent = None

        # test before any action
        result = REMOTE_COMMANDS['status'][FUNCTION](agent)

        self.assertTrue(len(result) == 1)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result['status'] == SUCCESS)
