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
''' The following class BuildAgent provides access commands to communicate
    with a BuildAgent without the need to now the detailed commands.
'''

from snakebuild.communication.client import Client
from snakebuild.communication.commandstructure import SUCCESS


class BuildAgentError(BaseException):
    ''' The base execpetion for all errors thrown within the BuildAgent
        class.
    '''


class BuildAgentRemoteError(BuildAgentError):
    ''' The base exception of the errors of the remote server. '''


class BuildAgentIllegalParameterError(BuildAgentError):
    ''' The error thrown if a method is called with an illegal paramter. '''


class BuildAgent(object):
    ''' This instance allows communicating with a build agent with simple
        methods there is no knowledge of the protocol necessary.
    '''

    def __init__(self, url, port):
        ''' Init the agent object to communicate with the agent later on

            @param url: The url of the server to connect to
            @param port: The network port where the server is listening.
        '''
        self.client = Client(url, port)

    def get_status(self):
        ''' Get the status information about the build agent.

            The answer of this command is a list if successfull otherwise an
            Exception is thrown with the error message stored.

            @return: If successfull it will return a list with a dictionary
                    for each resource.
        '''
        cmd, answ = self.client.send(Client.SJSON, 'status', None)
        if answ['status'] == SUCCESS:
            return answ['agent']
        raise BuildAgentRemoteError("[{0}]: {1}".format(cmd,
                answ['message']))
