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

from snakebuild.remote.resourceserver import ResourceServer, \
        ResourceServerRemoteError, ResourceServerIllegalParameterError
from snakebuild.communication.client import ClientCommunicationException
from test_helpers.versioneddir_helper import create_versioned_dir_all


class TestResourceServer(unittest.TestCase):
    ''' The unit test for the snake build resource server remote commands.
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

        resource_config = _create_resource_configs()
        _create_server_config(self.config_dir, resource_config)

    def tearDown(self):
        ''' Ensure that the server is stoped. '''
        subprocess.call([self.server_bin, 'stop'])

    def test_status_list_cmd(self):
        ''' Test the status list command function.
        '''
        rsrc_srvr = ResourceServer('localhost', _NETWORK_PORT)
        with self.assertRaises(ClientCommunicationException):
            rsrc_srvr.get_status_list()

        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
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

        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
        time.sleep(0.2)

        self.assertTrue(type(rsrc_srvr.get_resource_details('Test1')) == dict)
        # TODO check in more details

        # not existing resource should get an error back
        with self.assertRaises(ResourceServerRemoteError):
            rsrc_srvr.get_resource_details('Test11')
        # TODO check in more details

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))

    def test_acquire_releaes_resource(self):
        ''' Test the acquire_resource and release_resource commands.
        '''
        rsrc_srvr = ResourceServer('localhost', _NETWORK_PORT)
        with self.assertRaises(ClientCommunicationException):
            rsrc_srvr.acquire_resource('mytest', 'test1', False)

        # test if the parameters checks are in place
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource(12.2, 'test1', False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource('mytest', True, False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.acquire_resource('mytest', 'test1', 12)
        # the same for the release command
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.release_resource(12.2, 'test1', False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.release_resource('mytest', True, False)
        with self.assertRaises(ResourceServerIllegalParameterError):
            rsrc_srvr.release_resource('mytest', 'test1', 12)

        # now do the tests with the server running
        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
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

        with self.assertRaises(ResourceServerRemoteError):
            name = rsrc_srvr.acquire_resource('mytest', 'test11', False)
        with self.assertRaises(ResourceServerRemoteError):
            name = rsrc_srvr.release_resource('mytest2', 'test1', False)
        with self.assertRaises(ResourceServerRemoteError):
            name = rsrc_srvr.release_resource('mytest', 'test11', False)
        with self.assertRaises(ResourceServerRemoteError):
            name = rsrc_srvr.release_resource('mytest', 'test1', False)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))


_NETWORK_PORT = 9998


def _create_server_config(config_dir, resource_options):
    ''' Create the config file for the resource server.

        @param config_dir: The path where to store the config file
        @param resource_options: The informatin for the resource config
    '''
    sfl = open(os.path.join(config_dir, 'server.conf'), 'w')
    sfl.write('[resourceserver]\n')
    sfl.write('repository_type=GIT\n')
    sfl.write('resource_repos_name=commands\n')
    sfl.write('repository_local={0}\n'.format(resource_options[0]))
    sfl.write('repository_data={0}\n'.format(resource_options[1]))
    sfl.write('port = {0}\n'.format(_NETWORK_PORT))

    return os.path.join(config_dir, 'resources')


def _create_resource_configs():
    ''' Create the resources files for the resources used for this tests.

        @return: return the repository path and the repos config as a tuple
    '''
    repo, bare_dir = create_versioned_dir_all('commands')
    data = {"name": "Test1",
            "parallel_count": 2,
            "keywords": ["myTest", "build"],
            "parameters": {"value1": "arther"}}
    tfile = open(repo.get_local_path('test1.resource'), 'w')
    tfile.write(json.dumps(data))
    tfile.close()
    repo.add('test1.resource')

    data = {"name": "Test2",
            "parallel_count": 4,
            "keywords": ["myTest", "build", "run"],
            "parameters": {"value1": "trillian"}}
    tfile = open(repo.get_local_path('test2.resource'), 'w')
    tfile.write(json.dumps(data))
    tfile.close()
    repo.add('test2.resource')
    repo.commit('Tester', 'test@snakebuild.org', 'added resourcemanager '
            'tests')
    repo.push_remote()
    return repo.path, bare_dir
