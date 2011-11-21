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
''' The unit tests for the helper functions and enums for the command
    structure.
'''

import unittest

from snakebuild.communication.commandstructure import prepare_error,\
        prepare_answer, FUNCTION, DESCRIPTION, PARAMETERS,\
        PARAMETER_DESCRIPTIONS, SIGNED, ERROR, SUCCESS, CommandStructureError


class TestCommandStructure(unittest.TestCase):
    ''' The unit test for helper functions and enums of the remote
        communication command structures.
    '''
    def setUp(self):
        pass

    def test_prepare_error(self):
        ''' Test the prepare_error function. '''
        value = prepare_error('Test')
        self.assertTrue(type(value) == dict)
        self.assertTrue(len(value) == 2)
        self.assertTrue('status' in value)
        self.assertTrue('message' in value)
        self.assertTrue(value['status'] == ERROR)
        self.assertTrue(value['message'] == 'Test')

        value = prepare_error('Arther Dent')
        self.assertTrue(type(value) == dict)
        self.assertTrue(len(value) == 2)
        self.assertTrue('status' in value)
        self.assertTrue('message' in value)
        self.assertTrue(value['status'] == ERROR)
        self.assertTrue(value['message'] == 'Arther Dent')

    def test_prepare_answer(self):
        ''' Test the prepare_answer function. '''
        value = prepare_answer()
        self.assertTrue(type(value) == dict)
        self.assertTrue(len(value) == 1)
        self.assertTrue('status' in value)
        self.assertTrue(value['status'] == SUCCESS)

        value = prepare_answer({'value': 'Arther Dent'})
        self.assertTrue(type(value) == dict)
        self.assertTrue(len(value) == 2)
        self.assertTrue('status' in value)
        self.assertTrue('value' in value)
        self.assertTrue(value['status'] == SUCCESS)
        self.assertTrue(value['value'] == 'Arther Dent')

        value = prepare_answer({'value': 'Arther Dent', 'value2': 'Trinity'})
        self.assertTrue(type(value) == dict)
        self.assertTrue(len(value) == 3)
        self.assertTrue('status' in value)
        self.assertTrue('value' in value)
        self.assertTrue('value2' in value)
        self.assertTrue(value['status'] == SUCCESS)
        self.assertTrue(value['value'] == 'Arther Dent')
        self.assertTrue(value['value2'] == 'Trinity')

        with self.assertRaises(CommandStructureError):
            value = prepare_answer('test')

        with self.assertRaises(CommandStructureError):
            value = prepare_answer(12.34)

        with self.assertRaises(CommandStructureError):
            value = prepare_answer(12)

    def test_enum_values(self):
        ''' Test if the enum values have the expected value. The value must be
            the same as described in the documentation.
        '''
        self.assertTrue(FUNCTION == 0)
        self.assertTrue(DESCRIPTION == 1)
        self.assertTrue(PARAMETERS == 2)
        self.assertTrue(PARAMETER_DESCRIPTIONS == 3)
        self.assertTrue(SIGNED == 4)

    def test_constantes(self):
        ''' Test if the constante value have the expected value. '''
        self.assertTrue(ERROR == 'error')
        self.assertTrue(SUCCESS == 'success')
