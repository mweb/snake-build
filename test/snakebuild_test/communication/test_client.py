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

from snakebuild.communication.client import Client, _receive, \
        ClientCommunicationException, _parse_sjson_data

from test_helpers.dummysocket import DummySocket


class TestClient(unittest.TestCase):
    ''' The unit test for the snake build communication Client class. '''
    def setUp(self):
        pass

    def test_parse_sjson_data(self):
        ''' Test the private method _parse_sjson_data.

            This method expectes to receive a socket and reads from this a
            sjson data string. This tests creates a mockup of a socket to
            provide the data.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1, 2, 3], 'element': 12,
            'others': 'Elephant'}}

        msg = json.dumps(data)
        length = len(msg)
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy_sock = DummySocket()
        dummy_sock.add_data(message_string)
        cmd, param = _parse_sjson_data(dummy_sock)
        self.assertTrue(cmd == data['cmd'])
        self.assertTrue(param == data['parameters'])

    def test_parse_sjson_illegal_data(self):
        ''' Test the private method _parse_sjson_data illegal data.

            This method expectes to receive a socket and reads from this a
            sjson data string. This tests creates a mockup of a socket to
            provide the data.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1, 2, 3], 'element': 12,
            'others': 'Elephant'}}

        msg = json.dumps(data)
        length = len(msg)
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg[:-12]

        dummy_sock = DummySocket()
        dummy_sock.add_data(message_string)
        # got wrong length of message (not all data available)
        with self.assertRaises(ClientCommunicationException):
            _parse_sjson_data(dummy_sock)

        length = len(msg) - 12
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg[:-12]
        dummy_sock.add_data(message_string)

        # got complete message but can't be pared as json
        with self.assertRaises(ValueError):
            _parse_sjson_data(dummy_sock)

    def test_parse_sjson_no_data(self):
        ''' Test the private method _parse_sjson_data empty message.

            This method expectes to receive a socket and reads from this a
            sjson data string. This tests creates a mockup of a socket to
            provide the data.
        '''
        message_string = chr(0) + chr(0) + chr(0) + chr(0)

        dummy_sock = DummySocket()
        dummy_sock.add_data(message_string)
        self.assertIsNone(_parse_sjson_data(dummy_sock))

    def test_receive_sjson(self):
        ''' Test the private method _receive. Receive a sjson message.

            This method expects a socket to receive the data. With this test
            we provide a dummy socket that provides the expected data.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1, 2, 3], 'element': 12,
            'others': 'Elephant'}}

        msg = json.dumps(data)
        length = len(msg)
        message_string = ('a' + chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy_sock = DummySocket()
        dummy_sock.add_data(message_string)
        cmd, param = _receive(dummy_sock)
        self.assertTrue(cmd == data['cmd'])
        self.assertTrue(param == data['parameters'])

    def test_receive_unknown(self):
        ''' Test the private method _receive. Receive a unknown type.

            This method expects a socket to receive the data. With this test
            we provide a dummy socket that provides the expected data.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1, 2, 3], 'element': 12,
            'others': 'Elephant'}}

        msg = json.dumps(data)
        length = len(msg)
        message_string = ('.' + chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy_sock = DummySocket()
        dummy_sock.add_data(message_string)
        with self.assertRaises(ClientCommunicationException):
            _receive(dummy_sock)
