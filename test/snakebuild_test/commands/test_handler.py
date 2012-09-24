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
import argparse

from snakebuild.commands import handle_cmd, command, register_argument_parsers


class TestHandler(unittest.TestCase):
    ''' The unit test for the snake build common command handler functions.
    '''
    def setUp(self):
        ''' Setup the test case. '''
        pass

    def test_handle_cmd(self):
        ''' Test the handle_cmd for the common command handling.
        '''
        parser = argparse.ArgumentParser()
        register_argument_parsers(parser)

        args = parser.parse_args(['test1'])
        self.assertTrue(handle_cmd(args, None))
        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test1', 'param1'])

        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test2'])
        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test2', 'param1', 'param2'])
        args = parser.parse_args(['test2', 'param1'])
        self.assertTrue(handle_cmd(args, None))

        args = parser.parse_args(['test3'])
        self.assertTrue(handle_cmd(args, None))
        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test3', 'param1', 'param2'])
        args = parser.parse_args(['test3', '--param1', 'value1'])
        self.assertTrue(handle_cmd(args, None))

        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test4'])
        args = parser.parse_args(['test4', 'param1'])
        self.assertTrue(handle_cmd(args, None))
        args = parser.parse_args(['test4', 'param1', '--param2', 'value2'])
        self.assertTrue(handle_cmd(args, None))

        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test5'])
        with self.assertRaises(SystemExit):
            args = parser.parse_args(['test5', 'param1'])
        args = parser.parse_args(['test5', '12'])
        self.assertFalse(handle_cmd(args, None))
        self.assertTrue(handle_cmd(args, 10))


@command('test1', ())
def _test1(options, config):
    ''' The first test call
    '''
    return True


@command('test2', (
        (('param1',), {'help': 'The description of the first parameter'}),
    ))
def _test2(args, config):
    ''' The second test call with one parameter
    '''
    if args.param1 is None:
        raise Exception()
    return True


@command('test3', (
        (('--param1',), {'help': 'The description of the first parameter',
            'default': 12}),
    ))
def _test3(args, config):
    ''' The third test call with one optional parameter
        @param param1: The description of the first parameter
    '''
    if args.param1 is None:
        raise Exception()
    return True


@command('test4', (
        (('param1',), {'help': 'The description of the first parameter'}),
        (('--param2',), {'help': 'The description of the second parameter',
            'default': 12})
    ))
def _test4(args, config):
    ''' The fourth test call with two parameters one is optional
    '''
    if args.param1 is None or args.param2 is None:
        raise Exception()
    return True


@command('test5', (
        (('param1',), {'help': 'The description of the first parameter',
            'type': int}),
    ))
def _test5(args, config):
    ''' The fifth test call with one parameter. This call is special since
        it check the parameter 1 the options and config values.
        @param param1: The description of the first parameter
    '''
    if not args.param1 == 12:
        return False

    if not config == 10:
        return False

    return True
