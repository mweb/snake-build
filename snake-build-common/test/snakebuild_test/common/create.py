# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' Create the test suite for the common classes. '''

import unittest

from test_config import TestConfig


def suite():
    ''' Get the test suite for the communication snakebuild classes. '''
    conf = unittest.TestLoader().loadTestsFromTestCase(TestConfig)

    return unittest.TestSuite([conf])
