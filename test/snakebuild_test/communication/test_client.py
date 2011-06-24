# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' The unit tests for the Client object and its methods. '''

import unittest
import json

from snakebuild.communication.client import Client, _receive, \
        ClientCommunicationException, _prepare_sjson_data, _parse_sjson_data

from test_helpers.dummysocket import DummySocket


class TestClient(unittest.TestCase):
    ''' The unit test for the snake build communication Client class. '''
    def setUp(self):
        pass

    def test_prepare_sjson_data(self):
        ''' Test the private method _preapre_sjson_data.

            This method must create a message string with the full header
            and the json string to send.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1, 2, 3], 'element': 12,
            'others': 'Elephant'}}

        message = _prepare_sjson_data(data)

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
