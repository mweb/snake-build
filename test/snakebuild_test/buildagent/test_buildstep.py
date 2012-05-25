# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2012 Mathias Weber <mathew.weber@gmail.com>
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
''' The unit test for the build step object and the helper functions. '''

import unittest

from snakebuild.buildagent.buildstep import BuildStep, load_step, _is_valid


class TestBuildStep(unittest.TestCase):
    ''' The unit test for the snake build build step object
    '''
    def setUp(self):
        ''' Setup the test case. Create a directory for the test resources. If
            it allready exists remove it.
        '''
        pass

    def test_validation_check(self):
        ''' Test the _is_valid function to check if the given dictionary is
            valid.
        '''
        data = {}
        self.assertFalse(_is_valid(data))

        data['type'] = "test"
        self.assertFalse(_is_valid(data))

        data['name'] = "test"
        self.assertFalse(_is_valid(data))

        data['script'] = "gaga"
        self.assertFalse(_is_valid(data))

        data['input'] = {}
        self.assertFalse(_is_valid(data))

        data['output'] = {}
        self.assertFalse(_is_valid(data))

        data['checks'] = {}
        self.assertFalse(_is_valid(data))
        data['checks']['pre_condition'] = {}
        self.assertFalse(_is_valid(data))
        data['checks']['post_condition'] = {}
        self.assertFalse(_is_valid(data))
        data['checks']['log_check'] = "full"
        self.assertFalse(_is_valid(data))
        data['checks']['on_error'] = "abort"
        self.assertTrue(_is_valid(data))

        # now use wrong types
        data['type'] = 12.12
        self.assertFalse(_is_valid(data))
        data['type'] = "test"
        self.assertTrue(_is_valid(data))

        data['name'] = True
        self.assertFalse(_is_valid(data))
        data['name'] = "test"
        self.assertTrue(_is_valid(data))

        data['script'] = []
        self.assertFalse(_is_valid(data))
        data['script'] = "test"
        self.assertTrue(_is_valid(data))

        data['input'] = "test"
        self.assertFalse(_is_valid(data))
        data['input'] = {}
        self.assertTrue(_is_valid(data))

        data['output'] = 12
        self.assertFalse(_is_valid(data))
        data['output'] = {}
        self.assertTrue(_is_valid(data))

        data['checks']['pre_condition'] = "test"
        self.assertFalse(_is_valid(data))
        data['checks']['pre_condition'] = 12
        self.assertFalse(_is_valid(data))
        data['checks']['pre_condition'] = {}
        self.assertTrue(_is_valid(data))
        data['checks']['post_condition'] = "gaga"
        self.assertFalse(_is_valid(data))
        data['checks']['post_condition'] = 12
        self.assertFalse(_is_valid(data))
        data['checks']['post_condition'] = {}
        self.assertTrue(_is_valid(data))
        data['checks']['log_check'] = True
        self.assertFalse(_is_valid(data))
        data['checks']['log_check'] = 12.12
        self.assertFalse(_is_valid(data))
        data['checks']['log_check'] = "no"
        self.assertTrue(_is_valid(data))
        data['checks']['on_error'] = {}
        self.assertFalse(_is_valid(data))
        data['checks']['on_error'] = 42
        self.assertFalse(_is_valid(data))
        data['checks']['on_error'] = "Yes"
        self.assertTrue(_is_valid(data))

        tmp = data['checks']
        data['checks'] = 12.12
        self.assertFalse(_is_valid(data))
        data['checks'] = tmp
        self.assertTrue(_is_valid(data))

        # check input variables
        data['input']['VAR1'] = {}
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['type'] = "str"
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['description'] = "Variable One"
        self.assertTrue(_is_valid(data))
        data['input']['VAR1']['default'] = 12
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['default'] = "Value1"
        self.assertTrue(_is_valid(data))
        data['input']['VAR1']['type'] = "motorcycle"
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['type'] = "int"
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['default'] = 12
        self.assertTrue(_is_valid(data))
        data['input']['VAR1']['description'] = 12
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['description'] = "Variable One"
        self.assertTrue(_is_valid(data))
        data['input']['VAR1']['type'] = "float"
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['default'] = 12.12
        self.assertTrue(_is_valid(data))
        data['input']['VAR1']['type'] = 12
        self.assertFalse(_is_valid(data))
        data['input']['VAR1']['type'] = "float"
        self.assertTrue(_is_valid(data))

        # check output variables
        data['output']['VAR1'] = {}
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['type'] = "str"
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['description'] = "Variable One"
        self.assertTrue(_is_valid(data))
        data['output']['VAR1']['default'] = "Value1"
        self.assertTrue(_is_valid(data))
        data['output']['VAR1']['type'] = "motorcycle"
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['type'] = "int"
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['default'] = 12
        self.assertTrue(_is_valid(data))
        data['output']['VAR1']['description'] = 12
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['description'] = "Variable One"
        self.assertTrue(_is_valid(data))
        data['output']['VAR1']['type'] = "float"
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['default'] = 12.12
        self.assertTrue(_is_valid(data))
        data['output']['VAR1']['type'] = 12
        self.assertFalse(_is_valid(data))
        data['output']['VAR1']['type'] = "float"
        self.assertTrue(_is_valid(data))
