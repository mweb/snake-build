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
import tempfile
import json
import os
import shutil

from snakebuild.buildagent.buildstep import BuildStepException, load_step
from snakebuild.buildagent.buildstep.buildstep import _is_valid, \
        _get_env_values, _check_value, _parse_output_file, _check_input_values


class TestBuildStep(unittest.TestCase):
    ''' The unit test for the snake build build step object
    '''

    def setUp(self):
        ''' Setup the test case. Create a directory for the test resources.
            If it allready exists remove it.
        '''
        script = ('#!/bin/sh\n'
            'echo $VAR1\n')
        directory = tempfile.mkdtemp()
        self.script_filename = os.path.join(directory, 'simple.sh')
        self.step_filename = os.path.join(directory, 'simple.step')
        self.invalid_step_filename = os.path.join(directory, 'invalid.step')
        buildstep = {
                'name': 'SimpleTest',
                'description': 'Simple step for testing',
                'type': 'undefined',
                'script': self.script_filename,
                'input': {
                },
                'output': {},
                'checks': {
                    'log_check': 'none',
                    'on_error': 'abort'
                }
            }
        invalid_buildstep = {
                'description': 'Simple step for testing',
                'script': self.script_filename,
                'output': {},
                'checks': {
                    'log_check': 'none',
                    'on_error': 'abort'
                }
            }
        with open(self.script_filename, 'w') as sfl:
            sfl.write(script)
        with open(self.step_filename, 'w') as cfl:
            cfl.write(json.dumps(buildstep))
        with open(self.invalid_step_filename, 'w') as cfl:
            cfl.write(json.dumps(invalid_buildstep))

    def tearDown(self):
        ''' Remove the temporary directory with all its files. '''
        if os.path.isdir(os.path.dirname(self.script_filename)):
            shutil.rmtree(os.path.dirname(self.script_filename))

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

    def test_load_step(self):
        ''' Test the load_step function with illegal values. '''
        with self.assertRaises(BuildStepException):
            load_step(os.path.join(os.path.dirname(self.step_filename),
                    'nothing'))
        with self.assertRaises(BuildStepException):
            load_step(self.step_filename)
        with self.assertRaises(BuildStepException):
            load_step(self.invalid_step_filename)

    def test_get_env_values(self):
        ''' Test the generic method to get the environment values filled with
            the input values.
        '''
        test = {'INT1': {
                    'type': 'int',
                    'default': 12,
                    'description': ''
                },
                'INT2': {
                    'type': 'int',
                    'default': '42',
                    'description': ''
                },
                'INT3': {
                    'type': 'int',
                    'default': 33.2,
                    'description': ''
                },
                'FLOAT1': {
                    'type': 'float',
                    'default': 32.2,
                    'description': ''
                },
                'FLOAT2': {
                    'type': 'float',
                    'default': 33,
                    'description': ''
                },
                'FLOAT3': {
                    'type': 'float',
                    'default': '12.12',
                    'description': ''
                },
                'FLOAT4': {
                    'type': 'float',
                    'default': '14',
                    'description': ''
                },
                'BOOL1': {
                    'type': 'bool',
                    'default': True,
                    'description': ''
                },
                'BOOL2': {
                    'type': 'bool',
                    'default': 'True',
                    'description': ''
                },
                'BOOL3': {
                    'type': 'bool',
                    'default': '1',
                    'description': ''
                },
                'BOOL4': {
                    'type': 'bool',
                    'default': 'False',
                    'description': ''
                },
                'BOOL5': {
                    'type': 'bool',
                    'default': False,
                    'description': ''
                },
                'BOOL6': {
                    'type': 'bool',
                    'default': '0',
                    'description': ''
                },
                'STR1': {
                    'type': 'str',
                    'default': 0,
                    'description': ''
                },
                'STR2': {
                    'type': 'str',
                    'default': 'ASDF',
                    'description': ''
                },
                'NO_DEFAULT': {
                    'type': 'int',
                    'description': ''
                }
            }

        value = _get_env_values({'NO_DEFAULT': 12}, test)
        self.assertTrue(value['INT1'] == '12')
        self.assertTrue(value['INT2'] == '42')
        self.assertTrue(value['INT3'] == '33')
        self.assertTrue(value['FLOAT1'] == '32.2')
        self.assertTrue(value['FLOAT2'] == '33')
        self.assertTrue(value['FLOAT3'] == '12.12')
        self.assertTrue(value['FLOAT4'] == '14')
        self.assertTrue(value['BOOL1'] == 'True')
        self.assertTrue(value['BOOL2'] == 'True')
        self.assertTrue(value['BOOL3'] == 'True')
        self.assertTrue(value['BOOL4'] == 'False')
        self.assertTrue(value['BOOL5'] == 'False')
        self.assertTrue(value['BOOL6'] == 'False')

        with self.assertRaises(BuildStepException):
            value = _get_env_values({'NO_DEFAULT': 'test'}, test)
        with self.assertRaises(BuildStepException):
            value = _get_env_values({}, test)

        test['NO_DEFAULT']['type'] = 'float'
        with self.assertRaises(BuildStepException):
            value = _get_env_values({'NO_DEFAULT': 'test'}, test)
        test['NO_DEFAULT']['type'] = 'bool'
        with self.assertRaises(BuildStepException):
            value = _get_env_values({'NO_DEFAULT': 'test'}, test)

    def test_check_input_values(self):
        ''' Test the generic method to test all the input value against
            the expected input values.
        '''
        test = {'INT1': {
                    'type': 'int',
                    'default': 12,
                    'description': ''
                },
                'INT2': {
                    'type': 'int',
                    'default': '42',
                    'description': ''
                },
                'INT3': {
                    'type': 'int',
                    'default': 33.2,
                    'description': ''
                },
                'FLOAT1': {
                    'type': 'float',
                    'default': 32.2,
                    'description': ''
                },
                'FLOAT2': {
                    'type': 'float',
                    'default': 33,
                    'description': ''
                },
                'FLOAT3': {
                    'type': 'float',
                    'default': '12.12',
                    'description': ''
                },
                'FLOAT4': {
                    'type': 'float',
                    'default': '14',
                    'description': ''
                },
                'BOOL1': {
                    'type': 'bool',
                    'default': True,
                    'description': ''
                },
                'BOOL2': {
                    'type': 'bool',
                    'default': 'True',
                    'description': ''
                },
                'BOOL3': {
                    'type': 'bool',
                    'default': '1',
                    'description': ''
                },
                'BOOL4': {
                    'type': 'bool',
                    'default': 'False',
                    'description': ''
                },
                'BOOL5': {
                    'type': 'bool',
                    'default': False,
                    'description': ''
                },
                'BOOL6': {
                    'type': 'bool',
                    'default': '0',
                    'description': ''
                },
                'STR1': {
                    'type': 'str',
                    'default': 0,
                    'description': ''
                },
                'STR2': {
                    'type': 'str',
                    'default': 'ASDF',
                    'description': ''
                },
                'NO_DEFAULT': {
                    'type': 'int',
                    'description': ''
                }
            }

        value = _check_input_values({'NO_DEFAULT': 12}, test)
        self.assertTrue(value['INT1'] == 12)
        self.assertTrue(value['INT2'] == 42)
        self.assertTrue(value['INT3'] == 33)
        self.assertTrue(value['FLOAT1'] == 32.2)
        self.assertTrue(value['FLOAT2'] == 33)
        self.assertTrue(value['FLOAT3'] == 12.12)
        self.assertTrue(value['FLOAT4'] == 14)
        self.assertTrue(value['BOOL1'] is True)
        self.assertTrue(value['BOOL2'] is True)
        self.assertTrue(value['BOOL3'] is True)
        self.assertTrue(value['BOOL4'] is False)
        self.assertTrue(value['BOOL5'] is False)
        self.assertTrue(value['BOOL6'] is False)
        self.assertTrue(value['STR1'] == '0')
        self.assertTrue(value['STR2'] == 'ASDF')
        self.assertTrue(value['NO_DEFAULT'] == 12)

        with self.assertRaises(BuildStepException):
            value = _check_input_values({}, test)
        with self.assertRaises(BuildStepException):
            value = _check_input_values({'NO_DEFAULT': 'test'}, test)

        test['NO_DEFAULT']['type'] = 'int'
        with self.assertRaises(BuildStepException):
            value = _check_input_values({'NO_DEFAULT': 'test'}, test)
        test['NO_DEFAULT']['type'] = 'bool'
        with self.assertRaises(BuildStepException):
            value = _check_input_values({'NO_DEFAULT': 'test'}, test)

    def test_parse_output_file(self):
        ''' Test the parse output file helper function. '''
        test = {'INT1': {
                    'type': 'int',
                    'default': 12,
                    'description': ''
                },
                'INT2': {
                    'type': 'int',
                    'description': ''
                },
                'INT3': {
                    'type': 'int',
                    'description': ''
                },
                'FLOAT1': {
                    'type': 'float',
                    'default': 32.2,
                    'description': ''
                },
                'FLOAT2': {
                    'type': 'float',
                    'description': ''
                },
                'FLOAT3': {
                    'type': 'float',
                    'description': ''
                },
                'FLOAT4': {
                    'type': 'float',
                    'description': ''
                },
                'BOOL1': {
                    'type': 'bool',
                    'default': True,
                    'description': ''
                },
                'BOOL2': {
                    'type': 'bool',
                    'description': ''
                },
                'BOOL3': {
                    'type': 'bool',
                    'description': ''
                },
                'BOOL4': {
                    'type': 'bool',
                    'description': ''
                },
                'BOOL5': {
                    'type': 'bool',
                    'description': ''
                },
                'STR1': {
                    'type': 'str',
                    'default': 'TEST',
                    'description': ''
                },
                'STR2': {
                    'type': 'str',
                    'description': ''
                }
            }
        tempfile_name = ''
        with tempfile.NamedTemporaryFile(delete=False) as resultfile:
            tempfile_name = resultfile.name
            resultfile.write('INT2=42\n')
            resultfile.write('INT3=12\n')
            resultfile.write('FLOAT2=12.3\n')
            resultfile.write('FLOAT3=33\n')
            resultfile.write('FLOAT4=231.111\n')
            resultfile.write('BOOL2=True\n')
            resultfile.write('BOOL3=False\n')
            resultfile.write('BOOL4=1\n')
            resultfile.write('BOOL5=0\n')
            resultfile.write('STR2=HELLO\n')

        value = _parse_output_file(tempfile_name, test)
        self.assertTrue(value['INT1'] == 12)
        self.assertTrue(value['INT2'] == 42)
        self.assertTrue(value['INT3'] == 12)
        self.assertTrue(value['FLOAT1'] == 32.2)
        self.assertTrue(value['FLOAT2'] == 12.3)
        self.assertTrue(value['FLOAT3'] == 33)
        self.assertTrue(value['FLOAT4'] == 231.111)
        self.assertTrue(value['BOOL1'] is True)
        self.assertTrue(value['BOOL2'] is True)
        self.assertTrue(value['BOOL3'] is False)
        self.assertTrue(value['BOOL4'] is True)
        self.assertTrue(value['BOOL5'] is False)
        self.assertTrue(value['STR1'] == 'TEST')
        self.assertTrue(value['STR2'] == 'HELLO')

        with open(tempfile_name, 'a') as resultfile:
            resultfile.write('INT2=gg42\n')
        with self.assertRaises(BuildStepException):
            value = _parse_output_file(tempfile_name, test)

        with open(tempfile_name, 'w') as resultfile:
            resultfile.write('INT2=42\n')
        with self.assertRaises(BuildStepException):
            value = _parse_output_file(tempfile_name, test)

        os.remove(tempfile_name)

    def test_check_value(self):
        ''' Test the internal _check_value function. '''
        # int values
        self.assertTrue(_check_value('12', {'type': 'int'}) == 12)
        with self.assertRaises(BuildStepException):
            _check_value('13.2', {'type': 'int'})
        with self.assertRaises(BuildStepException):
            _check_value('meta', {'type': 'int'})

        # float values
        self.assertTrue(_check_value('12', {'type': 'float'}) == 12)
        self.assertTrue(_check_value('12.123', {'type': 'float'}) == 12.123)
        with self.assertRaises(BuildStepException):
            _check_value('meta', {'type': 'float'})

        # boolean values
        self.assertTrue(_check_value('0', {'type': 'bool'}) is False)
        self.assertTrue(_check_value('1', {'type': 'bool'}) is True)
        self.assertTrue(_check_value('False', {'type': 'bool'}) is False)
        self.assertTrue(_check_value('True', {'type': 'bool'}) is True)
        self.assertTrue(_check_value('false', {'type': 'bool'}) is False)
        self.assertTrue(_check_value('true', {'type': 'bool'}) is True)
        with self.assertRaises(BuildStepException):
            _check_value('meta', {'type': 'bool'})
        with self.assertRaises(BuildStepException):
            _check_value('2', {'type': 'bool'})
        with self.assertRaises(BuildStepException):
            _check_value('123.33', {'type': 'bool'})

        # string values
        self.assertTrue(_check_value('TEST', {'type': 'str'}) == 'TEST')
        with self.assertRaises(BuildStepException):
            _check_value(u'äöü', {'type': 'str'})

        # unknown type
        with self.assertRaises(BuildStepException):
            _check_value('TEST', {'type': 'UNKNOWN'})
