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
''' The unit test for the Config object '''

import unittest

from snakebuild.common import user_data_dir, shared_data_dir, \
        shared_config_dir, tmp_data_dir, log_dir


class TestAppdirs(unittest.TestCase):
    ''' The unit test for the snake build appdirs functions. '''
    def setUp(self):
        pass

    def test_tmp_data_dir(self):
        ''' Get a directory to store temporary data. The result might be 
            different on each platform.
        '''
        pass
