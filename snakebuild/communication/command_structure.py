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
''' This file describes the command structure supported by the message
    handler. This includes methods to prepare some basic answers.

    The commands dictionary provided to the message handler must have the
    following format:
    { 'CMD_NAME': (FUNCTION, 'DESCRIPTION', ['PARAMETER_LIST'],
        {'PARAM_NAME': 'PARAM_DESCRIPTION'}, True/False}

    CMD_NAME: The name of the command all letters in lower case

    FUNCTION: The function/method to call when such a command comes in.
    DESCRIPTION: The description of the function for documentation purposes.
    PARAMETERS_LIST: Each parameter is required to be string element within
        this list. The parameters must be all lower case.
    PARAM_NAME: For each parameter from the PARAMETERS_LIST we require the
        name here again.
    PARAM_DESCRIPTION: The description of the paramter.
    True/False: If set to True then this command can only be called from an
        instance which could sign the message correctly (This are usually
        commands which should only be called from verified sources
        (administrativ tasks)

    If there are optional paramters just write their name within square
    bracket. Example:
    [test]
'''


class CommandStructureError(BaseException):
    ''' The error that gets thrown if an answer could not be created. '''


# the access enums for the commands used within the message handler.
FUNCTION, DESCRIPTION, PARAMETERS, PARAMTER_DESCRIPTIONS, SIGNED = range(5)


def prepare_error(message):
    ''' Return a dictionary with a valid error message. This always has the
        following structure:

        { 'status': 'error', 'message': 'Error information'}

        The error information are the message whicht are provided with the
        call of this function. The message should be a human readable message
        string.

        It is allowed to add more paramters to the error string but this are
        the minimum required parameters.

        @param message: The message that belongs to the error
    '''
    return {'status': 'error', 'message': message}


def prepare_answer(data=None):
    ''' This call provides a dictionary with the minimal required parameter.
        All other data can be provided up front as the paramter (must be a
        dictionary or the results might be added to the resulting dictionary
        after the call.
    '''
    if data is None:
        return {'status': 'success'}
    if type(data) is dict:
        data['status'] = 'success'
        return data
    else:
        raise CommandStructureError('The given data for the answer data is '
                'not a dictionary.i')
