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

from snakebuild.commands import handle_cmd
from snakebuild.commands.handler import HandleCmdException
from snakebuild.common import Config


class TestHandler(unittest.TestCase):
    ''' The unit test for the snake build common command handler functions.
    '''
    def setUp(self):
        ''' Setup the test case. '''
        self.cmd_list = {'test1': (_test1, 'The first test command',
                    [], {}),
                'test2': (_test2, 'The second test command', ['TEST'],
                    {'TEST': 'param 1'}),
                'test3': (_test3, 'The third test command', ['[TEST]'],
                    {'[TEST]': 'param 1'}),
                'test4': (_test4, 'The fourth test command', ['TEST', '[OPT]'],
                    {'TEST': 'param 1', '[OPT]': 'param 2'}),
                'test5': (_test5, 'The fifth test command', ['TEST'],
                    {'TEST': 'param 1'})}

    def test_help_commands(self):
        ''' Test the handle_cmd with the help command.
        '''
        self.assertTrue(handle_cmd(['help'], None, None, self.cmd_list))
        self.assertFalse(handle_cmd(['help', 'other'], None, None,
                self.cmd_list))
        self.assertTrue(handle_cmd(['help', 'test1'], None, None,
                self.cmd_list))
        self.assertTrue(handle_cmd(['help', 'help'], None, None,
                self.cmd_list))

        config = Config()
        self.assertTrue(handle_cmd(['help', 'configfile'], None, config,
                self.cmd_list))
        self.assertTrue(handle_cmd([], None, None, self.cmd_list))
        with self.assertRaises(HandleCmdException):
            handle_cmd(['ping'], None, None, self.cmd_list)

    def test_handle_cmd(self):
        ''' Test the handle_cmd for the common command handling.
        '''
        self.assertTrue(handle_cmd(['test1'], None, None, self.cmd_list))
        self.assertFalse(handle_cmd(['test1', 'param1'], None, None,
                self.cmd_list))

        self.assertFalse(handle_cmd(['test2'], None, None, self.cmd_list))
        self.assertTrue(handle_cmd(['test2', 'param1'], None, None,
                self.cmd_list))
        self.assertFalse(handle_cmd(['test2', 'param1', 'param3'], None, None,
                self.cmd_list))

        self.assertTrue(handle_cmd(['test3'], None, None, self.cmd_list))
        self.assertTrue(handle_cmd(['test3', 'param1'], None, None,
                self.cmd_list))
        self.assertFalse(handle_cmd(['test3', 'param1', 'param3'], None, None,
                self.cmd_list))

        self.assertFalse(handle_cmd(['test4'], None, None, self.cmd_list))
        self.assertTrue(handle_cmd(['test4', 'param1'], None, None,
                self.cmd_list))
        self.assertTrue(handle_cmd(['test4', 'param1', 'param3'], None, None,
                self.cmd_list))

        self.assertFalse(handle_cmd(['test5', 'param1'], None, None,
                self.cmd_list))
        self.assertFalse(handle_cmd(['test5', 12], None, None,
                self.cmd_list))
        self.assertFalse(handle_cmd(['test5', 12], 11, None, self.cmd_list))
        self.assertTrue(handle_cmd(['test5', 12], 11, 10, self.cmd_list))


def _test1(cmd, options, config):
    ''' The first test call '''
    return True


def _test2(cmd, options, config, param1):
    ''' The second test call with one parameter '''
    return True


def _test3(cmd, options, config, param1=12):
    ''' The third test call with one optional parameter '''
    return True


def _test4(cmd, options, config, param1, param2=12):
    ''' The fourth test call with two parameters one is optional '''
    return True


def _test5(cmd, options, config, param1):
    ''' The fifth test call with one parameter. This call is special since
        it check the parameter 1 the options and config values.
    '''
    if not param1 == 12:
        return False

    if not options == 11:
        return

    if not config == 10:
        return False

    return True
