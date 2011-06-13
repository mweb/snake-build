# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest

from snakebuild.communication.messagehandler import MessageHandler

from test_helpers.dummysocket import DummySocket


class TestMessageHandler(unittest.TestCase):
    ''' The unit test for the snake build communication Server class. '''
    def setUp(self):
        pass

    def test_handle_cmd(self):
        ''' Test the private method of the message handler class. '''
        dummy = DummySocket()
        hdlr = MessageHandler(dummy, None, None)
        self.got_handled = {'cmd': None, 'parameters': None}
        hdlr._handle_cmd('test', [1, 2, 3], {'test': (self._handle_call_back,)})
        self.assertTrue(self.got_handled['cmd'] == 'test')
        self.assertTrue(self.got_handled['parameters'] == [1, 2, 3])

    def _handle_call_back(self, cmd, parameters):
        ''' Used as call back for the _handle_cmd. '''
        self.got_handled['cmd'] = cmd
        self.got_handled['parameters'] = parameters
