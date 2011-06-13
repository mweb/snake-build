# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest

from test_client import TestClient
from test_server import TestServer


def suite():
    ''' Get the test suite for the communication snakebuild classes. '''
    client = unittest.TestLoader().loadTestsFromTestCase(TestClient)
    server = unittest.TestLoader().loadTestsFromTestCase(TestServer)

    return unittest.TestSuite([client, server])
