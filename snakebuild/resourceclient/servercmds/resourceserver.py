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
''' The following class ResourceServer provides access commands to communicate
    with the ResourceServer without the need to now the detailed commands.
'''

from snakebuild.communication.client import Client
from snakebuild.communication.commandstructure import SUCCESS


class ResourceServerRemoteError(BaseException):
    ''' The base exception of the errors of the remote server. '''


class ResourceServer(object):
    ''' This instance allows communicating with a resouce server with simple
        methods there is not knowledge of the protocol necessary.
    '''

    def __init__(self, url, port):
        ''' Init the server object to communicate with the server later on

            @param url: The url of the server to connect to
            @param port: The network port where the server is listening.
        '''
        self.client = Client(url, port)

    def get_status_list(self):
        ''' Get the status information about all the configured resources.

            The answer of this command is a list if successfull otherwise an
            Exception is thrown with the error message stored.
            The answer list has one entry for each resource and each resource
            is stored within a dictionary with the following informations
            (keys):
            name: The name of the resource
            slots: The number of parallel slots configured
            free: The number of free slots
            users: The list of user names currently using the resource

            @return: If successfull it will return a list with a dictionary
                    for each resource.
        '''
        cmd, answ = self.client.send(Client.SJSON, 'status_list', None)
        if answ['status'] == SUCCESS:
            return answ['resources']
        raise ResourceServerRemoteError("[%s]: %s" % (cmd, answ['message']))
