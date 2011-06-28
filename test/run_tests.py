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
import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(
        os.path.realpath(sys.argv[0])), '..')))

import snakebuild_test


if __name__ == '__main__':
    snakebuild = snakebuild_test.suite()
    alltests = unittest.TestSuite([snakebuild])
    unittest.TextTestRunner(verbosity=2).run(alltests)
