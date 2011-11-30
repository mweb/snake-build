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
import subprocess

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
        config_file = os.path.join(self.config_dir, 'client.conf')
        config_data_file = os.path.join(os.path.dirname(__file__), '..', '..',
                '..', 'data', 'resourceclient.conf')
        self.server_bin = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                '..', 'bin', 'sb-resourceserver'))
        self.config = Config()
        self.config.init_default_config(config_data_file)
        self.config.load(config_file)

        # write server.conf file
        sfl = open(os.path.join(self.config_dir, 'server.conf'), 'w')
        sfl.write('[resourceserver]\n')
        sfl.write('resource_directory={0:s}\n'.format(
                os.path.join(self.config_dir, 'resources')))
        sfl.write('port = 9999\n')
        # write client.conf
        sfl = open(os.path.join(self.config_dir, 'client.conf'), 'w')
        sfl.write('[resourceclient]\n')
        sfl.write('resource_directory={0:s}\n'.format(
                os.path.join(self.config_dir, 'resources')))
        sfl.write('port = 9999\n')

    def test_status_cmd(self):
        ''' Test the status command function.
        '''
        self.assertTrue('status' in COMMANDS)
        self.assertTrue(COMMANDS['status'][0]("none", None, self.config) \
                == None)
        #self.assertTrue(COMMANDS['status'][0]("status", None, self.config) \
         #       == None)
        self.assertTrue(0 == subprocess.call([self.server_bin, 'start',
                '--background', '-f',
                '{0:s}'.format(os.path.join(self.config_dir, 'server.conf'))]))

        self.assertTrue(COMMANDS['status'][0]("status", None, self.config) \
                == True)

        self.assertTrue(0 == subprocess.call([self.server_bin, 'stop']))
