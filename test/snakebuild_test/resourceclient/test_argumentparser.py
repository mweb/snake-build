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
''' The unit test for the resource client argument parser. '''

import unittest

from snakebuild.resourceclient.commandlineparser import parse_command_line


class TestArgumentParser(unittest.TestCase):
    ''' The unit test for the snake build resourceclient argument parser.
    '''
    def setUp(self):
        ''' Setup the test case. Nothing to do here.
        '''
        pass

    def test_arguments_details(self):
        ''' Test the argumentparser for the details command of the client.
        '''
        result = parse_command_line(['details', 'Test1'], 'TestingV')
        self.assertTrue(result.command == 'details')
        self.assertTrue(result.name == 'Test1')
        self.assertTrue(result.configfile == None)
        self.assertTrue(result.username == None)
        self.assertTrue(result.server == None)
        self.assertTrue(result.port == None)

        result = parse_command_line(['--configfile', 'testfile',
                '--username', 'Arther', '--server', 'remote',
                '--port', '1234', 'details', 'Test1'], 'TestingV')
        self.assertTrue(result.command == 'details')
        self.assertTrue(result.name == 'Test1')
        self.assertTrue(result.configfile == 'testfile')
        self.assertTrue(result.username == 'Arther')
        self.assertTrue(result.server == 'remote')
        self.assertTrue(result.port == 1234)

    def test_arguments_status(self):
        ''' Test the argumentparser for the status command of the client.
        '''
        result = parse_command_line(['status'], 'TestingV')
        self.assertTrue(result.command == 'status')
        self.assertTrue(result.configfile == None)
        self.assertTrue(result.username == None)
        self.assertTrue(result.server == None)
        self.assertTrue(result.port == None)

        result = parse_command_line(['--configfile', 'testfile',
                '--username', 'Arther', '--server', 'remote',
                '--port', '1234', 'status'], 'TestingV')
        self.assertTrue(result.command == 'status')
        self.assertTrue(result.configfile == 'testfile')
        self.assertTrue(result.username == 'Arther')
        self.assertTrue(result.server == 'remote')
        self.assertTrue(result.port == 1234)

    def test_arguments_acquire(self):
        ''' Test the argumentparser for the acquire command of the client.
        '''
        result = parse_command_line(['acquire', 'Test1'], 'TestingV')
        self.assertTrue(result.command == 'acquire')
        self.assertTrue(result.tag == 'Test1')
        self.assertTrue(result.exclusive == False)
        self.assertTrue(result.configfile == None)
        self.assertTrue(result.username == None)
        self.assertTrue(result.server == None)
        self.assertTrue(result.port == None)

        result = parse_command_line(['acquire', 'Test1', '--exclusive'],
                'TestingV')
        self.assertTrue(result.command == 'acquire')
        self.assertTrue(result.tag == 'Test1')
        self.assertTrue(result.exclusive)
        self.assertTrue(result.configfile == None)
        self.assertTrue(result.username == None)
        self.assertTrue(result.server == None)
        self.assertTrue(result.port == None)

        result = parse_command_line(['--configfile', 'testfile',
                '--username', 'Arther', '--server', 'remote',
                '--port', '1234', 'acquire', 'Test1'], 'TestingV')
        self.assertTrue(result.command == 'acquire')
        self.assertTrue(result.tag == 'Test1')
        self.assertTrue(result.exclusive == False)
        self.assertTrue(result.configfile == 'testfile')
        self.assertTrue(result.username == 'Arther')
        self.assertTrue(result.server == 'remote')
        self.assertTrue(result.port == 1234)

        result = parse_command_line(['--configfile', 'testfile',
                '--username', 'Arther', '--server', 'remote',
                '--port', '1234', 'acquire', 'Test1', '--exclusive'],
                'TestingV')
        self.assertTrue(result.command == 'acquire')
        self.assertTrue(result.tag == 'Test1')
        self.assertTrue(result.exclusive)
        self.assertTrue(result.configfile == 'testfile')
        self.assertTrue(result.username == 'Arther')
        self.assertTrue(result.server == 'remote')
        self.assertTrue(result.port == 1234)

    def test_arguments_release(self):
        ''' Test the argumentparser for the release command of the client.
        '''
        result = parse_command_line(['release', 'Test1'], 'TestingV')
        self.assertTrue(result.command == 'release')
        self.assertTrue(result.name == 'Test1')
        self.assertTrue(result.exclusive == False)
        self.assertTrue(result.configfile == None)
        self.assertTrue(result.username == None)
        self.assertTrue(result.server == None)
        self.assertTrue(result.port == None)

        result = parse_command_line(['release', 'Test1', '--exclusive'],
                'TestingV')
        self.assertTrue(result.command == 'release')
        self.assertTrue(result.name == 'Test1')
        self.assertTrue(result.exclusive)
        self.assertTrue(result.configfile == None)
        self.assertTrue(result.username == None)
        self.assertTrue(result.server == None)
        self.assertTrue(result.port == None)

        result = parse_command_line(['--configfile', 'testfile',
                '--username', 'Arther', '--server', 'remote',
                '--port', '1234', 'release', 'Test1'], 'TestingV')
        self.assertTrue(result.command == 'release')
        self.assertTrue(result.name == 'Test1')
        self.assertTrue(result.exclusive == False)
        self.assertTrue(result.configfile == 'testfile')
        self.assertTrue(result.username == 'Arther')
        self.assertTrue(result.server == 'remote')
        self.assertTrue(result.port == 1234)

        result = parse_command_line(['--configfile', 'testfile',
                '--username', 'Arther', '--server', 'remote',
                '--port', '1234', 'release', 'Test1', '--exclusive'],
                'TestingV')
        self.assertTrue(result.command == 'release')
        self.assertTrue(result.name == 'Test1')
        self.assertTrue(result.exclusive)
        self.assertTrue(result.configfile == 'testfile')
        self.assertTrue(result.username == 'Arther')
        self.assertTrue(result.server == 'remote')
        self.assertTrue(result.port == 1234)
