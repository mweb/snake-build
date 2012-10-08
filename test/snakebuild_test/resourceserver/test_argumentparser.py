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
''' The unit test for the resource server argument parser. '''

import unittest

from snakebuild.resourceserver.commandlineparser import parse_command_line


class TestArgumentParser(unittest.TestCase):
    ''' The unit test for the snake build resourceserver argument parser.
    '''
    def setUp(self):
        ''' Setup the test case. Nothing to do here.
        '''
        pass

    def test_arguments_start(self):
        ''' Test the argumentparser for the start command of the server.
        '''
        result = parse_command_line(['start'], 'TestingV')
        print "\n"*5
        print "Got: %s" % result.name
        print "%s" % str(result)

        self.assertTrue(result.command == 'start')
        self.assertTrue(result.name == 'resourceserver')
        self.assertTrue(result.tag == 'master')
        self.assertTrue(result.background == False)
        self.assertTrue(result.configfile == None)

        result = parse_command_line(['--configfile', 'testfile',
                'start', '--background', '--tag', 'tag_one', '--name',
                'name_one'], 'TestingV')
        self.assertTrue(result.command == 'start')
        self.assertTrue(result.name == 'name_one')
        self.assertTrue(result.tag == 'tag_one')
        self.assertTrue(result.background)
        self.assertTrue(result.configfile == 'testfile')

    def test_arguments_stop(self):
        ''' Test the argumentparser for the stop command of the server.
        '''
        result = parse_command_line(['stop'], 'TestingV')
        self.assertTrue(result.command == 'stop')
        self.assertTrue(result.name == 'resourceserver')
        self.assertTrue(result.configfile == None)

        result = parse_command_line(['--configfile', 'testfile',
                'stop', '--name', 'name_one'], 'TestingV')
        self.assertTrue(result.command == 'stop')
        self.assertTrue(result.name == 'name_one')
        self.assertTrue(result.configfile == 'testfile')
