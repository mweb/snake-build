# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' Create the snakebuild_test suite '''

import unittest

import communication
import common


def suite():
    ''' Get the test suite for the common snakebuild classes. '''
    communication_test = communication.suite()
    common_test = common.suite()

    return unittest.TestSuite([communication_test, common_test])
