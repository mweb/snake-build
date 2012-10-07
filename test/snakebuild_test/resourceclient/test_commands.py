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

from snakebuild.resourceclient.clientcmds import *
from snakebuild.commands.handler import SHELL_COMMANDS
from snakebuild.common import Config
from test_helpers.versioneddir_helper import create_versioned_dir_all


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

        resource_config = _create_resource_configs()
        _create_server_config(self.config_dir, resource_config)
        config_file = _create_client_config(self.config_dir)

        self.config = Config()
        self.config.init_default_config(config_data_file)
        self.config.load(config_file)

    def test_status_cmd(self):
        ''' Test the status command function.
        '''
        self.assertTrue('status' in SHELL_COMMANDS)
        self.assertTrue(
                SHELL_COMMANDS['status'][0](None, self.config) == False)
        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
        time.sleep(0.2)
        self.assertTrue(SHELL_COMMANDS['status'][0](None, self.config) \
                == True)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))

    def test_details_cmd(self):
        ''' Test the status command function.
        '''
        args = _Options()
        args.name = 'Test1'
        args.exclusive = False

        self.assertTrue('details' in SHELL_COMMANDS)
        self.assertFalse(SHELL_COMMANDS['details'][0](args, self.config))
        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
        time.sleep(0.2)
        self.assertTrue(SHELL_COMMANDS['details'][0](args, self.config))

        # ask for a not existing resource
        args.name = 'Test11'
        self.assertFalse(SHELL_COMMANDS['details'][0](args, self.config))

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))

    def test_acquire_release_cmd(self):
        ''' Test the acquire and the release command functions.
        '''
        args = _Options()
        args.tag = 'Test1'
        args.name = 'Test1'
        args.exclusive = False

        self.assertTrue('acquire' in SHELL_COMMANDS)
        self.assertTrue('release' in SHELL_COMMANDS)

        self.assertFalse(SHELL_COMMANDS['acquire'][0](args, self.config))
        self.assertFalse(SHELL_COMMANDS['release'][0](args, self.config))

        self.assertTrue(0 == subprocess.call([self.server_bin, '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf')),
                'start', '--background']))
        time.sleep(0.2)

        # normal acquire release
        self.assertTrue(SHELL_COMMANDS['acquire'][0](args, self.config))
        self.assertTrue(SHELL_COMMANDS['release'][0](args, self.config))

        # exclusive acquire, release
        args.exclusive = True
        self.assertTrue(SHELL_COMMANDS['acquire'][0](args, self.config))
        self.assertTrue(SHELL_COMMANDS['release'][0](args, self.config))
        args.exclusive = False
        self.assertTrue(SHELL_COMMANDS['release'][0](args, self.config))

        # acquire, release (of not existing resource)
        args.tag = 'Test11'
        args.name = 'Test11'
        self.assertFalse(SHELL_COMMANDS['acquire'][0](args, self.config))
        self.assertFalse(SHELL_COMMANDS['release'][0](args, self.config))

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))


_NETWORK_PORT = 9999


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


def _create_client_config(config_dir):
    ''' Create the config file for the resource server.

        @param config_dir: The path where to store the config file

        @return: The path of the client config file
    '''
    sfl = open(os.path.join(config_dir, 'client.conf'), 'w')
    sfl.write('[resourceclient]\n')
    sfl.write('port = {0}\n'.format(_NETWORK_PORT))

    return os.path.join(config_dir, 'client.conf')


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


class _Options(object):
    ''' A dummy class for the options '''
    username = None
