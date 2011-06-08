# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest

from test_common import TestCommon


def suite():
    ''' Get the test suite for the common snakebuild classes. '''
    common = unittest.TestLoader().loadTestsFromTestCase(TestCommon)

    return unittest.TestSuite([common])
