# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest
import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(
        os.path.realpath(sys.argv[0])), '..')))

import snakebuild


if __name__ == '__main__':
    snakebuild = snakebuild.suite()
    alltests = unittest.TestSuite([snakebuild])
    unittest.TextTestRunner(verbosity=2).run(alltests)
