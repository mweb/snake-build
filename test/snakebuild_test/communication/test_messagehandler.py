# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest
import json

from snakebuild.communication.messagehandler import MessageHandler, _handle_cmd

from test_helpers.dummysocket import DummySocket
from test_helpers.dummycontainer import DummyContainer


class TestMessageHandler(unittest.TestCase):
    ''' The unit test for the snake build communication Server class. '''
    def setUp(self):
        self.got_handled = {'cmd': None, 'parameters': None}

    def test_handle_request(self):
        ''' Test the handle method of the message handler. '''
        data = {'cmd': 'test', 'parameters': {'Test': [1, 2],
                'Other': 'Quack'}}
        self.got_handled = {'cmd': None, 'parameters': None}
        msg = json.dumps(data)
        length = len(msg)
        message_string = ('a' + chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy = DummySocket()
        dummy.add_data(message_string)
        dummy.server = DummyContainer()
        dummy.server.commands = {'test': (self._handle_call_back,)}

        MessageHandler(dummy, None, None)
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['parameters'] == data['parameters'])

    def test_parse_sjson_request(self):
        ''' Test the private method _parse_sjson_request. '''
        data = {'cmd': 'test', 'parameters': {'Test': [1, 2],
                'Other': 'Quack'}}
        self.got_handled = {'cmd': None, 'parameters': None}
        msg = json.dumps(data)
        length = len(msg)
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy = DummySocket()
        dummy.server = DummyContainer()
        dummy.server.commands = {'test': (self._handle_call_back,)}

        hdlr = MessageHandler(dummy, None, None)
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['parameters'] == data['parameters'])

    def test_handle_cmd(self):
        ''' Test the private method of the message handler class. '''
        self.got_handled = {'cmd': None, 'parameters': None}
        _handle_cmd('test', [1, 2, 3],
                {'test': (self._handle_call_back,)})
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['parameters'] == [1, 2, 3])

    def _handle_call_back(self, cmd, parameters):
        ''' Used as call back for the _handle_cmd. '''
        self.got_handled['cmd'] = cmd
        self.got_handled['parameters'] = parameters
