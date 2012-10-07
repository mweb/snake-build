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
''' Create the test suite for the resourceclient classes. '''

import unittest

from test_commands import TestCommands
from test_client import TestClient
from test_argumentparser import TestArgumentParser


def suite():
    ''' Get the test suite for the resourceserver snakebuild classes. '''
    commands = unittest.TestLoader().loadTestsFromTestCase(TestCommands)
    client = unittest.TestLoader().loadTestsFromTestCase(TestClient)
    parser = unittest.TestLoader().loadTestsFromTestCase(TestArgumentParser)

    return unittest.TestSuite([client, commands, parser])
