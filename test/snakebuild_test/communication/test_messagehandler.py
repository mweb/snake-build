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
import json

from snakebuild.communication.messagehandler import MessageHandler, _handle_cmd
from snakebuild.communication.commandstructure import prepare_answer, \
        prepare_error

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

        hdlr = MessageHandler(dummy, None, None)
        hdlr.server = DummyContainer()
        hdlr.server.commands = {'test': (self._handle_call_back, '',
                ['Test', 'Other'], {}, False)}
        hdlr.server.data = "PING"
        dummy.add_data(message_string)
        hdlr.handle()
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['Test'] == [1, 2])
        self.assertTrue(self.got_handled['Other'] == 'Quack')
        self.assertTrue(self.got_handled['data'] == 'PING')

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

        hdlr = MessageHandler(dummy, None, None)
        hdlr.server = DummyContainer()
        hdlr.server.commands = {'test': (self._handle_call_back, '',
                ['Test', 'Other'], {}, False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['Test'] == [1, 2])
        self.assertTrue(self.got_handled['Other'] == 'Quack')
        self.assertTrue(self.got_handled['data'] == 16.7)

    def test_handle_cmd(self):
        ''' Test the private method of the message handler class. '''
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('test', {'p1': 1, 'p2': 2, 'p3': 3},
                {'test': (self._handle_call_back, '', ['p1', 'p2', '[p3]'], {},
                    False)}, 12, False)
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['p1'] == 1)
        self.assertTrue(self.got_handled['p2'] == 2)
        self.assertTrue(self.got_handled['p3'] == 3)
        self.assertTrue(self.got_handled['data'] == 12)
        self.assertTrue(answ['status'] == 'success')

    def _handle_call_back(self, cmd, data, Test=None, Other=None, p1=None, p2=None, p3=None):
        ''' Used as call back for the _handle_cmd. '''
        self.got_handled['cmd'] = cmd
        self.got_handled['Test'] = Test
        self.got_handled['Other'] = Other
        self.got_handled['p1'] = p1
        self.got_handled['p2'] = p2
        self.got_handled['p3'] = p3
        self.got_handled['data'] = data
        return prepare_answer()
