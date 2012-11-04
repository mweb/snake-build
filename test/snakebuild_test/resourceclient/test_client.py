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
''' The unit test for the resource client run command. '''

import unittest
import os.path
import shutil
import subprocess
import time

from snakebuild.resourceclient.client import run_client
from snakebuild.common import Config

from test_commands import _create_resource_configs, _create_client_config,\
        _create_server_config


class TestClient(unittest.TestCase):
    ''' The unit test for the snake build resourceclient run command.
    '''
    def setUp(self):
        ''' Setup the test case. Nothing to do here.
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

        resource_config = _create_resource_configs()
        _create_server_config(self.config_dir, resource_config)
        config_file = _create_client_config(self.config_dir)

        self.config = Config()
        self.config.init_default_config(config_data_file)
        self.config.load(config_file)

    def test_run_cmd(self):
        ''' Test the run command of the client.
        '''
        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
        time.sleep(0.2)

        args = DummyArgs(None, None, None)
        args.command = 'status'
        self.assertTrue(run_client(args, self.config))

        args = DummyArgs('fritz', None, None)
        args.command = 'status'
        self.assertTrue(run_client(args, self.config))

        args = DummyArgs(None, 'other.local', None)
        args.command = 'status'
        self.assertFalse(run_client(args, self.config))

        args = DummyArgs(None, None, 9898)
        args.command = 'status'
        self.assertFalse(run_client(args, self.config))

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))


class DummyArgs(object):
    ''' Dummy object to run the commands '''
    def __init__(self, username, server, port):
        self.username = username
        self.server = server
        self.port = port
