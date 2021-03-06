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

import logging

from snakebuild.i18n import _
from snakebuild.buildagent.buildstep.buildstep import BuildStepException, \
        BuildStep, _get_env_values, _parse_output_file

LOG = logging.getLogger('snakebuild.buildagent.buildstep.pythonbuildstep')


class PythonBuildStep(BuildStep):
    ''' The build step calling python functions. '''

    def __init__(self, data):
        self.BuildStep.__init__(data)

        self.python_version = None
        if 'python_version' in data:
            self.python_version = data['python_version']

    def run(self, values):
        ''' Run this Build Step. To run it you need to provide a dictionary
            with all the input variables stored within a dictionary.
            This method will return a tuple with the result status and the
            dictionary with the output variables.

            @param values: the dictionary with all the entries for all input
                    variables.
            @return: (status, output_dictionary)
        '''
        pass
