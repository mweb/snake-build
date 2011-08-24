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
''' The unit tests for the Client object and its methods. '''

import unittest
import json

from snakebuild.communication.messages import prepare_sjson_data

from test_helpers.dummysocket import DummySocket


class TestMessages(unittest.TestCase):
    ''' The unit test for the snake build communication messages functions. '''
    def setUp(self):
        pass

    def test_prepare_sjson_data(self):
        ''' Test the private method _preapre_sjson_data.

            This method must create a message string with the full header
            and the json string to send.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1, 2, 3], 'element': 12,
            'others': 'Elephant'}}

        message = prepare_sjson_data(data)

        # check if messgae identifier is sjson 0x61 or 'a'
        self.assertTrue(ord(message[0]) == 0x61)

        length = ((ord(message[1]) << 24) + (ord(message[2]) << 16) +
                (ord(message[3]) << 8) + ord(message[4]))
        # check if the length of the message is as expected
        self.assertTrue((length + 5) == len(message))

        # reload the string as a json object and compare it with the data
        # object
        msg = json.loads(message[5:])
        for key, value in data.iteritems():
            self.assertTrue(key in msg)
            self.assertTrue(msg[key] == value)
