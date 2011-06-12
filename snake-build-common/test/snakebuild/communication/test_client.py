# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest
import copy

from snakebuild.communication import Client


class TestClient(unittest.TestCase):
    ''' The unit test for the snake build communication Client class. '''
    def setUp(self):
        pass

    def test_prepare_sjson_data(self):
        ''' Test the private method _preapre_sjson_data. This method must
            create a message string with the full header and the json string
            to send.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1,2,3], 'element': 12,
            'others': 'Elephant'}}
        orig = copy.deepcopy(data)

        cli = Client('', 22222)
        message = cli._prepare_sjson_data(data)
        res = 10
        self.assertTrue(res is None)

    def test_parse_sjson_data(self):
        ''' Test the private method _parse_sjson_data. This method expectes to 
            receive a socket and reads from this a sjson data string.
            This tests creates a mockup of a socket to provide the data.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1,2,3], 'element': 12,
            'others': 'Elephant'}}
        orig = copy.deepcopy(data)

        cli = Client('', 22222)
        # TODO
#        dummy_sock = DummySocket()
#        dummy_sock.add_data(message_string)
#        message = cli._parse_sjson_data(dummy_sock)

    def _test_receive(self):
        ''' Test the private method _receive. This method expects a socket to
            receive the data. With this test we provide a dummy socket that
            provides the expected data.
        '''
        data = {'cmd': 'test', 'parameters': {'list': [1,2,3], 'element': 12,
            'others': 'Elephant'}}
        orig = copy.deepcopy(data)

        cli = Client('', 22222)
        # TODO
#        dummy_sock = DummySocket()
#        dummy_sock.add_data(message_string)
#        message = cli._receive(dummy_sock)

