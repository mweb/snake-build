# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' Create the test suite for the common classes. '''

import unittest

from test_config import TestConfig
from test_output import TestOutput


def suite():
    ''' Get the test suite for the communication snakebuild classes. '''
    conf = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    out = unittest.TestLoader().loadTestsFromTestCase(TestOutput)

    return unittest.TestSuite([conf, out])
