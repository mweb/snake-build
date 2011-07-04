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

import unittest

from test_client import TestClient
from test_server import TestServer
from test_messagehandler import TestMessageHandler


def suite():
    ''' Get the test suite for the communication snakebuild classes. '''
    client = unittest.TestLoader().loadTestsFromTestCase(TestClient)
    server = unittest.TestLoader().loadTestsFromTestCase(TestServer)
    handler = unittest.TestLoader().loadTestsFromTestCase(TestMessageHandler)

    return unittest.TestSuite([client, server, handler])