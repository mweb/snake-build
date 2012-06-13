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

import json
import os
import logging
import subprocess

from snakebuild.i18n import _

LOG = logging.getLogger('snakebuild.buildagent.buildstep')


class BuildStepException(BaseException):
    ''' The exceptino that gets thrown if a problem arises during handling
        a buildstep.
    '''


def load_step(filename):
    ''' Load the given file and create the build step object.

        @param filename: The full path of the file to read.
    '''
    if not os.path.isfile(filename):
        LOG.error(_('The given build step file does not exist: {0}').
                format(filename))
        raise BuildStepException('The given build step file does not exist: '
                '{0}'.format(filename))

    bsf = open(filename, 'r')
    data = json.load(bsf)
    if _is_valid(data):
        if data["type"] == "shell":
            return ShellBuildStep(data)
        elif data["type"] == "python":
            return PythonBuildStep(data)
        else:
            LOG.error(_('The given build type for the build step is not '
                    'supported: {0} ({1})').format(data["type"], filename))
            raise BuildStepException('The given build type forthe build step '
                    'is not supported: {0} ({1})'.format(data["type"],
                    filename))
    else:
        LOG.error(_('The step file does not have a valid data structure: {0}').
                format(filename))
        raise BuildStepException('TThe step file does not have a valid data '
                'structure: {0}'.format(filename))


class BuildStep(object):
    ''' The generic build step defing the interface to use it. '''
    NOTHING, ILLEGAL_VALUES, ERROR, WARNING, ABORTED, SUCCESS = range(6)
    NOT_STARTED, STARTING, RUNNING, WAITING, STOPPING, FINISHED = range(6)

    def __init__(self, stepdesc):
        ''' Init the build step object from a json encoded file. '''
        self.name = stepdesc['name']
        self.description = stepdesc['description']
        self.script = stepdesc['script']
        self.input_vars = stepdesc['input']
        self.output_vars = stepdesc['output']

        # TODO do something more here
        self.pre_condition = stepdesc['checks']['pre_condition']
        self.post_condition = stepdesc['checks']['post_condition']
        self.log_check = stepdesc['checks']['log_check']
        self.on_error = stepdesc['checks']['on_error']

        self.result_status = self.NOTHING
        self.run_status = self.NOT_STARTED

    def run(self, values):
        ''' Run this Build Step. To run it you need to provide a dictionary
            with all the input variables stored within a dictionary.
            This method will return a tuple with the result status and the
            dictionary with the output variables.

            @param values: the dictionary with all the entries for all input
                    variables.
            @return: (status, output_dictionary)
        '''
        raise BuildStepException('NOT IMPLEMENTED')


class ShellBuildStep(BuildStep):
    ''' The build step running a shell script. '''

    def __init__(self, data):
        BuildStep.__init__(self, data)

        self.executable = '/bin/sh'
        if 'shell' in data:
            self.executable = data['shell']

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

        env_values = os.environ.copy()
        env_values.update(values)
        for name, description in self.input_vars.iteritems():
            if not name in values:
                if 'default' in description:
                    env_values[name] = description['default']
                else:
                    LOG.error(_('Not all required variable names are defined.'
                            ' Missing: {0}').format(name))
                    return BuildStep.ILLEGAL_VALUES

        log_checker = None
        if self.log_check.lower() == 'full':
            # TODO implementd the log cheker here
            pass

        # use line buffered mode
        with open(log_file_name, 'w') as logf:
            # TODO start the listening socket for the results
            self.run_status = BuildStep.RUNNING
            self.result_status = BuildStep.SUCCESS

            worker = subprocess.Popen([self.executable, self.script],
                    bufsize=1, stderr=subprocess.STDOUT, stdout=logf,
                    env=env_values)

            import time
            while worker.poll() is None:
                time.sleep(0.1)
                if log_checker is not None:
                    # TODO implementd the log checker here
                    pass

            self.run_status = BuildStep.FINISHED
            return (self.result_status, self.output_dictionary)

        LOG.error('could not create the output log file for the build step: '
                '{0}'.format(log_file_name))
        self.run_status = BuildStep.FINISHED
        self.result_status = BuildStep.ERROR
        return (self.result_status, {})


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


class Checks(object):
    ''' The input/output check handler '''


def _is_valid_variable(data):
    ''' Check if the given variable type is a valid which means it has at
        least a type and a description key and optional a default value.

        The type supports the following types:
            - str
            - int
            - float
    '''
    if not 'type' in data:
        return _("The variable 'type' is not specified.")
    if not 'description' in data:
        return  _("The variable 'description' is not specified.")

    if not isinstance(data['type'], (str, unicode)):
        return _("The variable 'type' is not a string.")
    if not isinstance(data['description'], (str, unicode)):
        return _("The variable 'description' is not a string.")

    if 'default' in data:
        if not data['type'] in ('str', 'int', 'float'):
            return _('The given variable type is not supported: {0}').\
                    format(data['type'])

        if (data['type'] == 'str' and
                not isinstance(data['default'], (str, unicode))):
            return _("The variable 'default' is not a string as specified.")
        elif data['type'] == 'int' and not isinstance(data['default'], int):
            return _("The variable 'default' is not a integer as specified.")
        elif (data['type'] == 'float' and
                not isinstance(data['default'], float)):
            return _("The variable 'default' is not a integer as specified.")
    return None


def _is_valid(data):
    ''' Check if the given buildstep dictionary has all required fields if not
        log the problem and return false.

        @param data: The data dictionary to use for the creation of the
                BuildStep object.

        @return True if valid and False if not
    '''
    if not "type" in data:
        LOG.error(_('The build step object does not have a build type.'))
        return False
    if not isinstance(data["type"], (str, unicode)):
        LOG.error(_('The type entry within the build step is not a string.'))
        return False

    if not "name" in data:
        LOG.error(_('The build step object does not have a name.'))
        return False
    if not isinstance(data["name"], (str, unicode)):
        LOG.error(_('The name entry within the build step is not a string.'))
        return False

    if not "script" in data:
        LOG.error(_('The build step object does not have a script entry.'))
        return False
    if not isinstance(data["script"], (str, unicode)):
        LOG.error(_('The script entry within the build step is not a string.'))
        return False

    if not "input" in data:
        LOG.error(_('The build step object does not have a input entry.'))
        return False
    if not isinstance(data["input"], dict):
        LOG.error(_('The input entry within the build step is not a '
                'dictionary.'))
        return False
    for name, description in data["input"].iteritems():
        answer = _is_valid_variable(description)
        if answer is not None:
            LOG.error(_('The variable: {0} is not correctly specified: {1}').
                    format(name, answer))
            return False

    if not "output" in data:
        LOG.error(_('The build step object does not have a output entry.'))
        return False
    if not isinstance(data["output"], dict):
        LOG.error(_('The output entry within the build step is not a '
                'dictionary.'))
        return False
    for name, description in data["output"].iteritems():
        answer = _is_valid_variable(description)
        if answer is not None:
            LOG.error(_('The variable: {0} is not correctly specified: {1}').
                    format(name, answer))
            return False

    if not "checks" in data:
        LOG.error(_('The build step object does not have a checks entry.'))
        return False
    if not isinstance(data["checks"], dict):
        LOG.error(_('The checks entry within the build step is not a '
                'dictionary.'))
        return False
    if not "pre_condition" in data["checks"]:
        LOG.error(_('The checks entry expects an object with the name '
                'pre_condition'))
        return False
    if not isinstance(data["checks"]["pre_condition"], dict):
        LOG.error(_('The pre_condition entry within checks is not a '
                'dictionary.'))
        return False
    if not "post_condition" in data["checks"]:
        LOG.error(_('The checks entry expects an object with the name '
                'post_condition'))
        return False
    if not isinstance(data["checks"]["post_condition"], dict):
        LOG.error(_('The post_condition entry within checks is not a '
                'dictionary.'))
        return False
    if not "log_check" in data["checks"]:
        LOG.error(_('The checks entry expects an object with the name '
                'log_check'))
        return False
    if not isinstance(data["checks"]["log_check"], (str, unicode)):
        LOG.error(_('The log_check entry within checks is not a string.'))
        return False
    if not "on_error" in data["checks"]:
        LOG.error(_('The checks entry expects an object with the name '
                'on_error'))
        return False
    if not isinstance(data["checks"]["on_error"], (str, unicode)):
        LOG.error(_('The on_error entry within checks is not a string.'))
        return False

    return True
