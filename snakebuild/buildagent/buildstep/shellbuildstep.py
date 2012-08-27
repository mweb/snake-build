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
''' The build steps for the build agent. '''

import os
import shutil
import logging
import subprocess
import tempfile

from snakebuild.i18n import _
from snakebuild.buildagent.buildstep.buildstep import BuildStepException, \
        BuildStep, _get_env_values, _parse_output_file

LOG = logging.getLogger('snakebuild.buildagent.buildstep.shellbuildstep')


class ShellBuildStep(BuildStep):
    ''' The build step running a shell script. '''
    SHELL_COMMANDS = ('#!/bin/sh\n\n'
            'echo $1=\\"$2\\" >> $SNAKEBUILD_RETURN')

    def __init__(self, data):
        BuildStep.__init__(self, data)
        self.tmp_storage_dir = tempfile.mkdtemp()

        self.executable = '/bin/sh'
        if 'shell' in data:
            self.executable = data['shell']

    def __del__(self):
        self._clean_up()
        BuildStep.__del__(self)

    def run(self, values, log_file_name):
        ''' Run this Build Step. To run it you need to provide a dictionary
            with all the input variables stored within a dictionary.
            This method will return a tuple with the result status and the
            dictionary with the output variables.

            @param values: the dictionary with all the entries for all input
                    variables.
            @param log_file_name: The name of the logfile to create for this
                    run this has to be the full path. If the file exists it
                    will be overwritten.
            @return: (status, output_dictionary)
        '''
        self.run_status = BuildStep.STARTING
        self.result_status = BuildStep.NOTHING
        self.output_dictionary = {}

        try:
            env_values = _get_env_values(values, self.input_vars)
        except BuildStepException, x:
            self.run_status = BuildStep.FINISHED
            self.result_status = BuildStep.ERROR
            raise x

        env_values = self._create_tmpfiles(env_values)

        log_checker = None
        if self.log_check.lower() == 'full':
            # TODO implementd the log cheker here
            pass

        # use line buffered mode
        try:
            with open(log_file_name, 'w') as logf:
                self.run_status = BuildStep.RUNNING
                self.result_status = BuildStep.SUCCESS

                worker = subprocess.Popen([self.executable, self.script],
                        bufsize=1, stderr=subprocess.STDOUT, stdout=logf,
                        env=env_values)

                while worker.poll() is None:
                    if log_checker is not None:
                        # TODO implementd the log checker here
                        pass

                self.run_status = BuildStep.FINISHED
                self.output_dictionary = _parse_output_file(
                        env_values['SNAKEBUILD_RETURN'], self.output_vars)
                return (self.result_status, self.output_dictionary)
        except IOError, x:
            LOG.error(_('could not create the output log file for the build '
                    'step: {0}:\n{1}').format(log_file_name, x))
            self.run_status = BuildStep.FINISHED
            self.result_status = BuildStep.ERROR
            raise BuildStepException('could not create the output log file '
                    'for the build step: {0}:\n{1}'.format(log_file_name, x))
        self.run_status = BuildStep.FINISHED
        self.result_status = BuildStep.ERROR
        return (self.result_status, {})

    def _create_tmpfiles(self, env_values):
        ''' Creates the temporary results directory and the bin directory for
            the custom commands. The directory will be created on run and
            will be removed at the end of the run.

            @param env_values: The dictionary with all the env values, the
                    PATH value will be changed.
        '''
        if os.path.isdir(self.tmp_storage_dir):
            shutil.rmtree(self.tmp_storage_dir)

        return_path = os.path.join(self.tmp_storage_dir, 'return')
        bin_path = os.path.join(self.tmp_storage_dir, 'bin')

        os.makedirs(return_path)
        os.makedirs(bin_path)

        with open(os.path.join(bin_path, 'sb_set'), 'w') as sbfile:
            os.chmod(os.path.join(bin_path, 'sb_set'), 0755)
            sbfile.write(self.SHELL_COMMANDS)

        env_values['SNAKEBUILD_RETURN'] = os.path.join(return_path, 'answer')
        env_values['PATH'] = '{0}:{1}'.format(bin_path, env_values['PATH'])
        return env_values

    def _clean_up(self):
        ''' clean up all temporary files '''
        if os.path.isdir(self.tmp_storage_dir):
            shutil.rmtree(self.tmp_storage_dir)
