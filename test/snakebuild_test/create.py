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
''' Create the snakebuild_test suite '''

import unittest

import communication
import common
import commands
import resourceserver
import resourceclient
import buildagent
import remote

def suite():
    ''' Get the test suite for the common snakebuild classes. '''
    communication_test = communication.suite()
    common_test = common.suite()
    commands_test = commands.suite()
    resourceserver_test = resourceserver.suite()
    resourceclient_test = resourceclient.suite()
    buildagent_test = buildagent.suite()
    remote_test = remote.suite()

    return unittest.TestSuite([communication_test, common_test, commands_test,
            resourceserver_test, resourceclient_test, buildagent_test,
            remote_test])
