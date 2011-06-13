# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest

from test_client import TestClient


def suite():
    ''' Get the test suite for the communication snakebuild classes. '''
    client = unittest.TestLoader().loadTestsFromTestCase(TestClient)

    return unittest.TestSuite([client])
