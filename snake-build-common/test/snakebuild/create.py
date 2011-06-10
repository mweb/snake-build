# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest

import communication


def suite():
    ''' Get the test suite for the common snakebuild classes. '''
    communication_test = communication.suite()

    return unittest.TestSuite([communication_test])
