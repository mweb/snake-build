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
import os

from snakebuild.communication.messagehandler import MessageHandler, _handle_cmd
from snakebuild.communication.commandstructure import prepare_answer

from test_helpers.dummysocket import DummySocket
from test_helpers.dummycontainer import DummyContainer
from test_helpers.logfile_helper import prepare_log_file, check_log_file


class TestMessageHandler(unittest.TestCase):
    ''' The unit test for the snake build communication Server class. '''
    def setUp(self):
        self.logfile = prepare_log_file()

        self.got_handled = {'cmd': None, 'parameters': None}

    def tearDown(self):
        ''' remove log file '''
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)

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
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = "PING"
        dummy.add_data(message_string)
        hdlr.handle()
        self.assertTrue(self.got_handled['Test'] == [1, 2])
        self.assertTrue(self.got_handled['Other'] == 'Quack')
        self.assertTrue(self.got_handled['data'] == 'PING')

    def test_handle_request_unsuported_type(self):
        ''' Test the handle method of the message handler use an unsupported
            type.
        '''
        data = {'cmd': 'test', 'parameters': {'Test': [1, 2],
                'Other': 'Quack'}}
        self.got_handled = {'cmd': None, 'parameters': None}
        msg = json.dumps(data)
        length = len(msg)
        message_string = ('c' + chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy = DummySocket()

        hdlr = MessageHandler(dummy, None, None)
        hdlr.server = DummyContainer()
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = "PING"
        dummy.add_data(message_string)
        hdlr.handle()
        self.assertTrue(check_log_file(self.logfile, 'The message type '
                'received is not supported. got: 0x63'))

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
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(self.got_handled['Test'] == [1, 2])
        self.assertTrue(self.got_handled['Other'] == 'Quack')
        self.assertTrue(self.got_handled['data'] == 16.7)

    def test_parse_sjson_request_illegal(self):
        ''' Test the private method _parse_sjson_request with illegal
            requests.
        '''
        length = 10
        # do not send enough bytes for the lenght
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256))

        dummy = DummySocket()

        hdlr = MessageHandler(dummy, None, None)
        hdlr.server = DummyContainer()
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(check_log_file(self.logfile, "The message received "
                "did not return 4 bytes for the length of the message: Got "
                "only: 3"))

        length = 10
        msg = "123"
        # do not send the right of bytes after the length
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy = DummySocket()

        hdlr = MessageHandler(dummy, None, None)
        hdlr.server = DummyContainer()
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(check_log_file(self.logfile, "Wrong length of data "
                "received: Expected 10 but got 3"))

        length = 5
        msg = "{12345"
        # do not send a json string
        message_string = (chr((length >> 24) % 256) +
                chr((length >> 16) % 256) + chr((length >> 8) % 256) +
                chr(length % 256)) + msg

        dummy = DummySocket()

        hdlr = MessageHandler(dummy, None, None)
        hdlr.server = DummyContainer()
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(check_log_file(self.logfile, "Could not parse the "
                "received data. Not a valid json string."))

        # test with illegal json string (no cmd)
        data = {'cmmd': 'test', 'parameters': {'Test': [1, 2],
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
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(check_log_file(self.logfile, "The message received "
                "did not have a 'cmd' key."))

        # test with illegal json string (no parameters)
        data = {'cmd': 'test', 'parammeters': {'Test': [1, 2],
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
        hdlr.server.commands = {'test': (self._handle_call_back,
                ['Test', 'Other'], False)}
        hdlr.server.data = 16.7
        dummy.add_data(message_string)
        hdlr._parse_sjson_request()
        self.assertTrue(check_log_file(self.logfile, "The message received "
                "did not have a 'parameters' key."))

    def test_handle_cmd(self):
        ''' Test the private method of the message handler class. '''
        # test command with no paramters
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('test', None,
                {'test': (self._handle_call_back, [],
                    False)}, 12, False)
        self.assertTrue(self.got_handled['data'] == 12)
        self.assertTrue(answ['status'] == 'success')

        # test command with paramters
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('test', {'p1': 1, 'p2': 2, 'p3': 3},
                {'test': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    False)}, 12, False)
        self.assertTrue(self.got_handled['p1'] == 1)
        self.assertTrue(self.got_handled['p2'] == 2)
        self.assertTrue(self.got_handled['p3'] == 3)
        self.assertTrue(self.got_handled['data'] == 12)
        self.assertTrue(answ['status'] == 'success')

        # wrong case for command (should still be handled)
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('TesT', {'p1': 2, 'p2': 3, 'p3': 4},
                {'test': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    False)}, 12, False)
        self.assertTrue(self.got_handled['p1'] == 2)
        self.assertTrue(self.got_handled['p2'] == 3)
        self.assertTrue(self.got_handled['p3'] == 4)
        self.assertTrue(self.got_handled['data'] == 12)
        self.assertTrue(answ['status'] == 'success')

        # wrong case for command list (should still be handled)
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('TesT', {'p1': 3, 'p2': 4, 'p3': 5},
                {'tESt': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    False)}, 12, False)
        self.assertTrue(self.got_handled['p1'] == 3)
        self.assertTrue(self.got_handled['p2'] == 4)
        self.assertTrue(self.got_handled['p3'] == 5)
        self.assertTrue(self.got_handled['data'] == 12)
        self.assertTrue(answ['status'] == 'success')

        # try to call a protected command (not allowed)
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('test', {'p1': 1, 'p2': 2, 'p3': 3},
                {'test': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    True)}, 12, False)
        self.assertTrue(answ['status'] == 'error')
        self.assertTrue(answ['message'].find('You are not allowed to call '
                'this command.') == 0)

        # missing parameter
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('test', {'p2': 2, 'p3': 3},
                {'test': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    False)}, 12, False)
        self.assertTrue(answ['status'] == 'error')
        self.assertTrue(answ['message'].find('The parameter (p1) is required '
                'for the call of this command, but is not available') == 0)

        # too many parameter
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('test', {'p1': 1, 'p4': 55, 'p2': 2, 'p3': 3},
                {'test': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    False)}, 12, False)
        self.assertTrue(answ['status'] == 'error')
        self.assertTrue(answ['message'].find('The parameter (p4) is not '
                'specified for the call of this command.') == 0)

        # not existing command
        self.got_handled = {'cmd': None, 'parameters': None}
        answ = _handle_cmd('tester', {'p1': 2, 'p2': 3, 'p3': 4},
                {'test': (self._handle_call_back, ['p1', 'p2', '[p3]'],
                    False)}, 12, False)

        self.assertTrue(answ['status'] == 'error')
        self.assertTrue(answ['message'].find('The requested command is not '
                'supported by this server instance. Command: tester') == 0)

    def _handle_call_back(self, data, Test=None, Other=None, p1=None, p2=None,
            p3=None):
        ''' Used as call back for the _handle_cmd. '''
        self.got_handled['Test'] = Test
        self.got_handled['Other'] = Other
        self.got_handled['p1'] = p1
        self.got_handled['p2'] = p2
        self.got_handled['p3'] = p3
        self.got_handled['data'] = data
        return prepare_answer()
