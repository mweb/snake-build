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
''' Create the test suite for the buildagent classes. '''

import unittest

from test_buildagent import TestBuildAgent
from test_buildstep import TestBuildStep, TestShellBuildStep
from test_commands import TestCommands


def suite():
    ''' Get the test suite for the buildagent classes. '''
    agent = unittest.TestLoader().loadTestsFromTestCase(TestBuildAgent)
    buildstep = unittest.TestLoader().loadTestsFromTestCase(TestBuildStep)
    shellbuildstep = unittest.TestLoader().loadTestsFromTestCase(
            TestShellBuildStep)
    commands = unittest.TestLoader().loadTestsFromTestCase(TestCommands)

    return unittest.TestSuite([agent, buildstep, shellbuildstep, commands])
