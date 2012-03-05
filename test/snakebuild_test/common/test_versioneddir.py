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
''' The unit test for the versioned directory class '''

import unittest

import snakebuild.common.versioneddir as vd


class TestVersionedDir(unittest.TestCase):
    ''' The unit test for the snake build common versioned dir classes. '''
    def setUp(self):
        ''' Setup the test case. '''
        pass

    def test_init(self):
        ''' Test the initialisation of the versioned directory.
        '''
        pass

    def test_git_commands(self):
        ''' Test the internal git command methods.
        '''
        versioned = vd.VersionedGitDir('/tmp/testrepos')
        self.assertTrue(versioned._gitr('branch') == 0)
