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
''' The unit test for the output functions '''

import unittest

from snakebuild.commands import handle_cmd, command
from snakebuild.commands.handler import HandleCmdException
from snakebuild.common import Config


class TestHandler(unittest.TestCase):
    ''' The unit test for the snake build common command handler functions.
    '''
    def setUp(self):
        ''' Setup the test case. '''
        pass

    def test_help_commands(self):
        ''' Test the handle_cmd with the help command.
        '''
        self.assertTrue(handle_cmd(['help'], None, None))
        self.assertFalse(handle_cmd(['help', 'other'], None, None))
        self.assertTrue(handle_cmd(['help', 'test1'], None, None))
        self.assertTrue(handle_cmd(['help', 'help'], None, None))

        config = Config()
        self.assertTrue(handle_cmd(['help', 'configfile'], None, config))
        self.assertTrue(handle_cmd([], None, None))
        self.assertFalse(handle_cmd(['ping'], None, None))

    def test_handle_cmd(self):
        ''' Test the handle_cmd for the common command handling.
        '''
        self.assertTrue(handle_cmd(['test1'], None, None))
        self.assertFalse(handle_cmd(['test1', 'param1'], None, None))

        self.assertFalse(handle_cmd(['test2'], None, None))
        self.assertTrue(handle_cmd(['test2', 'param1'], None, None))
        self.assertFalse(handle_cmd(['test2', 'param1', 'param3'], None, None))

        self.assertTrue(handle_cmd(['test3'], None, None))
        self.assertTrue(handle_cmd(['test3', 'param1'], None, None))
        self.assertFalse(handle_cmd(['test3', 'param1', 'param3'], None, None))

        self.assertFalse(handle_cmd(['test4'], None, None))
        self.assertTrue(handle_cmd(['test4', 'param1'], None, None))
        self.assertTrue(handle_cmd(['test4', 'param1', 'param3'], None, None))

        self.assertFalse(handle_cmd(['test5', 'param1'], None, None))
        self.assertFalse(handle_cmd(['test5', 12], None, None))
        self.assertFalse(handle_cmd(['test5', 12], 11, None))
        self.assertTrue(handle_cmd(['test5', 12], 11, 10))


@command('test1')
def _test1(options, config):
    ''' The first test call
    '''
    return True


@command('test2')
def _test2(options, config, param1):
    ''' The second test call with one parameter
        @param param1: The description of the first parameter
    '''
    return True


@command('test3')
def _test3(options, config, param1=12):
    ''' The third test call with one optional parameter 
        @param param1: The description of the first parameter
    '''
    return True


@command('test4')
def _test4(options, config, param1, param2=12):
    ''' The fourth test call with two parameters one is optional 
        @param param1: The description of the first parameter
        @param param2: The description of the second parameter
    '''
    return True


@command('test5')
def _test5(options, config, param1):
    ''' The fifth test call with one parameter. This call is special since
        it check the parameter 1 the options and config values.
        @param param1: The description of the first parameter
    '''
    if not param1 == 12:
        return False

    if not options == 11:
        return

    if not config == 10:
        return False

    return True
