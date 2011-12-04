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
''' The unit test for the resource client commands. '''

import unittest
import os.path
import shutil
import subprocess
import time
import json

from snakebuild.resourceclient.client_commands import COMMANDS
from snakebuild.common import Config


class TestCommands(unittest.TestCase):
    ''' The unit test for the snake build resourceclient commands.
    '''
    def setUp(self):
        ''' Setup the test case. Nothing to yet.
        '''
        self.config_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                'data', 'client_tests'))
        if os.path.isdir(self.config_dir):
            shutil.rmtree(os.path.join(self.config_dir))
        os.makedirs(os.path.join(self.config_dir))

        config_data_file = os.path.join(os.path.dirname(__file__), '..', '..',
                '..', 'data', 'resourceclient.conf')
        self.server_bin = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                '..', 'bin', 'sb-resourceserver'))

        resource_config_dir = _create_server_config(self.config_dir)
        config_file = _create_client_config(self.config_dir)
        _create_resource_configs(resource_config_dir)

        self.config = Config()
        self.config.init_default_config(config_data_file)
        self.config.load(config_file)

    def test_status_cmd(self):
        ''' Test the status command function.
        '''
        self.assertTrue('status' in COMMANDS)
        self.assertTrue(COMMANDS['status'][0]("none", None, self.config) \
                == None)
        self.assertTrue(COMMANDS['status'][0]("status", None, self.config) \
                == False)
        self.assertTrue(0 == subprocess.call([self.server_bin, 'start',
                '--background', '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf'))]))
        time.sleep(0.2)
        self.assertTrue(COMMANDS['status'][0]("status", None, self.config) \
                == True)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))

    def test_details_cmd(self):
        ''' Test the status command function.
        '''
        self.assertTrue('details' in COMMANDS)
        self.assertTrue(COMMANDS['details'][0]("none", None, self.config,
                None) == None)
        self.assertFalse(COMMANDS['details'][0]("details", None, self.config,
                'Test1'))
        self.assertTrue(0 == subprocess.call([self.server_bin, 'start',
                '--background', '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf'))]))
        time.sleep(0.2)
        self.assertTrue(COMMANDS['details'][0]("details", None, self.config,
                'Test1'))

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))


_NETWORK_PORT = 9999


def _create_server_config(config_dir):
    ''' Create the config file for the resource server.

        @param config_dir: The path where to store the config file

        @return: The path where the resources should be stored
    '''
    sfl = open(os.path.join(config_dir, 'server.conf'), 'w')
    sfl.write('[resourceserver]\n')
    sfl.write('resources_directory={0:s}\n'.format(
            os.path.join(config_dir, 'resources')))
    sfl.write('port = {0}\n'.format(_NETWORK_PORT))

    return os.path.join(config_dir, 'resources')


def _create_client_config(config_dir):
    ''' Create the config file for the resource server.

        @param config_dir: The path where to store the config file

        @return: The path of the client config file
    '''
    sfl = open(os.path.join(config_dir, 'client.conf'), 'w')
    sfl.write('[resourceclient]\n')
    sfl.write('port = {0}\n'.format(_NETWORK_PORT))

    return os.path.join(config_dir, 'client.conf')


def _create_resource_configs(path):
    ''' Create the resources files for the resources used for this tests.

        @param path: The path where to create the new files.
    '''
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)

    data = {"name": "Test1",
            "parallel_count": 2,
            "keywords": ["myTest", "build"],
            "parameters": {"value1": "arther"}}
    tfile = open(os.path.join(path, 'test1.resource'), 'w')
    tfile.write(json.dumps(data))
    tfile.close()

    data = {"name": "Test2",
            "parallel_count": 4,
            "keywords": ["myTest", "build", "run"],
            "parameters": {"value1": "trillian"}}
    tfile = open(os.path.join(path, 'test2.resource'), 'w')
    tfile.write(json.dumps(data))
