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
''' The unit test for the resource server remote library calls. '''

import unittest
import os.path
import shutil
import subprocess
import time
import json

from snakebuild.resourceclient.servercmds import ResourceServer, \
        ResourceServerRemoteError, ResourceServerIllegalParameterError
from snakebuild.communication.client import ClientCommunicationException
from snakebuild.common import Config


class TestServerCmds(unittest.TestCase):
    ''' The unit test for the snake build resource client remote commands.
    '''
    def setUp(self):
        ''' Setup the test case. Nothing yet.
        '''
        self.config_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                'data', 'client_tests'))
        if os.path.isdir(self.config_dir):
            shutil.rmtree(os.path.join(self.config_dir))
        os.makedirs(os.path.join(self.config_dir))

        self.server_bin = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                '..', 'bin', 'sb-resourceserver'))

        resource_config_dir = _create_server_config(self.config_dir)
        _create_resource_configs(resource_config_dir)

    def tearDown(self):
        ''' Ensure that the server is stoped. '''
        subprocess.call([self.server_bin, 'stop'])


    def test_status_list_cmd(self):
        ''' Test the status list command function.
        '''
        rsrc_srvr = ResourceServer('localhost', _NETWORK_PORT)
        with self.assertRaises(ClientCommunicationException):
            rsrc_srvr.get_status_list()

        self.assertTrue(0 == subprocess.call([self.server_bin, 'start',
                '--background', '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf'))]))
        time.sleep(0.2)

        self.assertTrue(type(rsrc_srvr.get_status_list()) == list)
        # TODO check in more details

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))

    def test_get_resource_details(self):
        ''' Test the get_resource_details command
        '''
        rsrc_srvr = ResourceServer('localhost', _NETWORK_PORT)
        with self.assertRaises(ClientCommunicationException):
            rsrc_srvr.get_resource_details('Test1')
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.get_resource_details(12)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'start',
                '--background', '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf'))]))
        time.sleep(0.2)

        self.assertTrue(type(rsrc_srvr.get_resource_details('Test1')) == dict)
        # TODO check in more details

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))

    def test_acquire_releaes_resource(self):
        ''' Test the acquire_resource and release_resource commands.
        '''
        rsrc_srvr = ResourceServer('localhost', _NETWORK_PORT)
        with self.assertRaises(ClientCommunicationException):
            rsrc_srvr.acquire_resource('mytest', 'test1', False)

        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource(12.2, 'test1', False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource('mytest', True, False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource('mytest', 'test1', 12)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'start',
                '--background', '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf'))]))
        time.sleep(0.2)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource(12.2, 'test1', False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource('mytest', True, False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource('mytest', 'test1', 12)

        name = rsrc_srvr.acquire_resource('mytest', 'test1', False)
        self.assertTrue(name == 'Test1')
        name = rsrc_srvr.release_resource('mytest', name, False)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))



_NETWORK_PORT = 9998


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
