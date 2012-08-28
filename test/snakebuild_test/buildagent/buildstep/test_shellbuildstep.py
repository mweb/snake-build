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
''' The unit test for the shell build step object and the helper functions. '''

import unittest
import tempfile
import json
import os
import shutil

from snakebuild.buildagent.buildstep import BuildStep, \
        BuildStepException, load_step


class TestShellBuildStep(unittest.TestCase):
    ''' The unit test for the snake shell build build step object
    '''
    def setUp(self):
        ''' Setup the test case. Create a directory for the test resources. If
            it allready exists remove it.
        '''
        script = ('#!/bin/sh\n'
            'echo $VAR1\n'
            'echo $VAR2\n'
            'sb_set VALUE "Test value"')
        directory = tempfile.mkdtemp()
        self.script_filename = os.path.join(directory, 'simple.sh')
        self.step_filename = os.path.join(directory, 'simple.step')
        buildstep = {
                'name': 'SimpleTest',
                'description': 'Simple step for testing',
                'type': 'shell',
                'shell': '/bin/sh',
                'script': self.script_filename,
                'input': {
                    'VAR1': {
                        'type': 'str',
                        'default': 'argone',
                        'description': ''
                    },
                    'VAR2': {
                        'type': 'int',
                        'default': 12,
                        'description': ''
                    }
                },
                'output': {},
                'checks': {
                    'pre_condition': {},
                    'post_condition': {},
                    'log_check': 'none',
                    'on_error': 'abort'
                }
            }
        with open(self.script_filename, 'w') as sfl:
            sfl.write(script)
        with open(self.step_filename, 'w') as cfl:
            cfl.write(json.dumps(buildstep))

    def tearDown(self):
        ''' Remove the temporary directory with all its files. '''
        if os.path.isdir(os.path.dirname(self.script_filename)):
            shutil.rmtree(os.path.dirname(self.script_filename))

    def test_shell_buildstep(self):
        ''' Test the ShellBuildStep class '''
        logfile = os.path.join(os.path.dirname(self.step_filename),
                'shelltest.log')

        step = load_step(self.step_filename)
        result = step.run({'VAR1': 'TEST'}, logfile)
        self.assertTrue(isinstance(result, tuple))
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[0] == BuildStep.SUCCESS)
        self.assertTrue('VALUE' in result[1])
        self.assertTrue(result[1]['VALUE'] == 'Test value')
        self.assertTrue('VALUE' in step.output_dictionary)
        self.assertTrue(step.output_dictionary['VALUE'] == 'Test value')

        with open(logfile, 'r') as lfl:
            self.assertTrue(lfl.readline().strip() == 'TEST')
            self.assertTrue(lfl.readline().strip() == '12')
        with self.assertRaises(BuildStepException):
            # log file exists already and is a directory --> Error
            result = step.run({'VAR1': 'TEST'},
                    os.path.dirname(self.step_filename))
        with self.assertRaises(BuildStepException):
            # illegal value for VAR2
            result = step.run({'VAR2': 'TEST'},
                    os.path.dirname(self.step_filename))
