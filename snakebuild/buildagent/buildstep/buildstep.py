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
import copy
import shutil
import logging
import subprocess
import tempfile

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
            from shellbuildstep import ShellBuildStep
            return ShellBuildStep(data)
        elif data["type"] == "python":
            from pythonbuildstep import PythonBuildStep
            return PythonBuildStep(data)
        elif data["type"] == "multi":
            from multibuildstep import MultiBuildStep
            return MultiBuildStep(data)
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


def _get_env_values(new_values, input_vars):
    ''' Get the os environment values and add input values for the input
        variables to the environment values.

        @param new_values: the dictionary with the values to check and add.
        @param input_vars: The input variables that need to be added.

        @return dictionary if everything is ok otherwise throw an
                exception.
    '''
    env_values = os.environ.copy()
    env_values.update(new_values)
    for name, description in input_vars.iteritems():
        if not name in new_values:
            if 'default' in description:
                new_values[name] = description['default']
            else:
                LOG.error(_('Not all required variable names are defined.'
                        ' Missing: {0}').format(name))
                raise BuildStepException('Not all required variable '
                        'names are defined. Missing: {0}'.format(name))

        try:
            # do not use the returned value since this could change float
            # values we prefere the string value over the real flota value.
            result = _check_value(new_values[name], description)
            if isinstance(result, (int, bool)):
                # we handle ints and boolean differently to get a consisten
                # result even for floats (on int) --> casted to int
                env_values[name] = str(result)
            else:
                env_values[name] = str(new_values[name])
        except BuildStepException, exc:
            LOG.error('{0} Value: {1}'.format(exc.message, name))
            raise BuildStepException('{0} Value: {1}'.format(exc.message,
                    name))

        env_values[name] = str(env_values[name])
    return env_values


def _check_input_values(values, input_vars):
    ''' Check the given values dictionary if it contains all the expected
        input values.

        @param values: The dictionary with the values to check if all required
                are available
        @param input_vars: The input value dictionary with all the types and
                default value informations.
    '''
    result = copy.deepcopy(values)
    for name, description in input_vars.iteritems():
        if not name in values:
            if 'default' in description:
                result[name] = description['default']
            else:
                LOG.error(_('Not all reuired variable names are defined. '
                        'Missing: {0}').format(name))
                raise BuildStepException('Not all required variable '
                        'names are defined. Missing: {0}'.format(name))
        result[name] = _check_value(result[name], description)
    return result

def _parse_output_file(filename, output_vars):
    ''' Parse the given output file. The values must be stored as key value
        pairs. Where as the key and value are seperated with a equal sign.
        The value might have double quotes to mark the beginning and the end
        of the value.
        If the value is stored in one line the double quotes are not
        necessary.

        @param filename: The file with the key value pairs.
        @param output_vars: The variables
        @return: a dictionary with the key value pairs.
    '''
    result = {}
    # parse file
    if os.path.isfile(filename):
        with open(filename, 'r') as retfile:
            for line in retfile.readlines():
                values = line.split('=')
                if len(values) == 2:
                    value = values[1].strip()
                    if value.startswith('"'):
                        value = value[1:]
                    if value.endswith('"'):
                        value = value[:-1]
                    result[values[0].strip()] = value

    # check with defined output variables
    for name, description in output_vars.iteritems():
        if not name in result:
            if 'default' in description:
                result[name] = description['default']
            else:
                LOG.error(_('Not all required variable names are defined.'
                        ' Missing: {0}').format(name))
                raise BuildStepException('Not all required variable '
                        'names are defined. Missing: {0}'.format(name))

        try:
            result[name] = _check_value(result[name], description)
        except BuildStepException, exc:
            LOG.error('{0} Value: {1}'.format(exc.message, name))
            raise BuildStepException('{0} Value: {1}'.format(exc.message,
                    name))

    return result


def _check_value(value, description):
    ''' Check if a given value matches the description.

        @param value
        @param description
        @return the input value (or the default value) as the expressed type
    '''
    if description['type'] == 'int':
        if not isinstance(value, int):
            try:
                return int(value)
            except ValueError:
                raise BuildStepException('The given string for the '
                        'value is not an int')
        return value
    elif description['type'] == 'float':
        if not isinstance(value, float):
            try:
                return float(value)
            except ValueError:
                raise BuildStepException('The given string for the value '
                        'is not a float')
        return value
    elif description['type'] == 'bool':
        if not isinstance(value, bool):
            if not value.lower() in ['true', 'false', '0', '1']:
                raise BuildStepException('The given string for the value '
                        'is not a boolean')
            if value.lower() in ['true', '1']:
                return True
            else:
                return False
        return value
    elif description['type'] == 'str':
        if not isinstance(value, str):
            try:
                return str(value)
            except ValueError:
                raise BuildStepException('The given value could not be '
                        'transformed to a string.')
        return value

    raise BuildStepException('The given type is not supported: "{0}"'.
            format(description['type']))
