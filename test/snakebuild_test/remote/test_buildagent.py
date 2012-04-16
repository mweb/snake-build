# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2012 Mathias Weber <mathew.weber@gmail.com>
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
''' The unit test for the build agent remote library calls. '''

import unittest
import os.path
import shutil
import subprocess

from snakebuild.remote.buildagent import BuildAgent, \
        BuildAgentRemoteError, BuildAgentIllegalParameterError
from snakebuild.communication.client import ClientCommunicationException


class TestBuildAgent(unittest.TestCase):
    ''' The unit test for the snake build agent remote commands.
    '''
    def setUp(self):
        ''' Setup the test case. Nothing yet.
        '''
        self.config_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                'data', 'buildagent_tests'))
        if os.path.isdir(self.config_dir):
            shutil.rmtree(os.path.join(self.config_dir))
        os.makedirs(os.path.join(self.config_dir))

        self.server_bin = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..',
                '..', 'bin', 'sb-buildagent'))

    def tearDown(self):
        ''' Ensure that the server is stoped. '''
        subprocess.call([self.server_bin, 'stop'])

    def test_status_cmd(self):
        ''' Test the status command function.
        '''
        pass
