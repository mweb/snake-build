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

from snakebuild.i18n import _
from snakebuild.communication.client import Client
from snakebuild.communication.commandstructure import SUCCESS


class ResourceServerError(BaseException):
    ''' The base execpetion for all errors thrown within the ResourceServer
        class.
    '''


class ResourceServerRemoteError(ResourceServerError):
    ''' The base exception of the errors of the remote server. '''


class ResourceServerIllegalParameterError(ResourceServerError):
    ''' The error thrown if a method is called with an illegal paramter. '''


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
        raise ResourceServerRemoteError("[{0}]: {1}".format(cmd,
                answ['message']))

    def get_resource_details(self, name):
        ''' Get the detail information about one resource.

            The answer of this command is a dictionary with all the
            information about one resource. The following keys are available:
            name: The name of the resource
            slots: The number of parallel slots configured
            free: The number of free slots
            users: The list of user names currently using the resource
            parameters: All the parameters (could be almost anything what json
                supports)

            @return: If successfull it will return a dictionary with all the
                    information about a resource.
        '''
        if not (type(name) is str or type(name) is unicode):
            raise ResourceServerIllegalParameterError(_('name parameter '
                    'requires a string as the value. {0}').format(type(name)))

        cmd, answ = self.client.send(Client.SJSON, 'resource_details',
                {'name': name})
        if answ['status'] == SUCCESS:
            return answ['resource']
        raise ResourceServerRemoteError("[{0}]: {1}".format(cmd,
                answ['message']))

    def acquire_resource(self, name, tag, exclusive=False):
        ''' Acquire a resource with a givne tag name. The name for the user to
            acquire the resource must be given. With the exclusive flag it is
            possible to acquire a resource exclusivly.

            @param name: The name of the user to acquire the given resource
            @param tag: The tag of the resource to get.
            @param exclusive: If set to true then the resource is needed for
                exclusive usage. Otherwise the number of parallel users is
                specified within the config.

            @return: If successfull it will return the name of the resource
        '''
        if not (type(name) is str or type(name) is unicode):
            raise ResourceServerIllegalParameterError(_('name parameter '
                    'requires a string as the value. {0}').format(type(name)))
        if not (type(tag) is str or type(tag) is unicode):
            raise ResourceServerIllegalParameterError(_('tag parameter '
                    'requires a string as the value. {0}').format(type(tag)))
        if type(exclusive) is not bool:
            raise ResourceServerIllegalParameterError(_('exclusive parameter '
                    'must be a boolean value and not: {0}').format(
                    type(exclusive)))

        cmd, answ = self.client.send(Client.SJSON, 'acquire',
                {'name': name, 'tag': tag, 'exclusive': exclusive})
        if answ['status'] == SUCCESS:
            return answ['resource']
        raise ResourceServerRemoteError("[{0}]: {1}".format(cmd,
                answ['message']))

    def release_resource(self, name, resource, exclusive=False):
        ''' Release the given resource. The name of the user that acquired the
            resource must be given and the exclusive flag defines if the
            resource should be release entirely or if only the exclusive lock
            should be released and one "normal" lock on the resource should be
            kept.

            @param name: The name of the user to release the given resource
            @param resource: The name of the resource to release.
            @param exclusive: If set to true then only release the exclusive
                lock but keep a "normal" lock.

            @return: If successfull it will return the name of the resource
        '''
        if not (type(name) is str or type(name) is unicode):
            raise ResourceServerIllegalParameterError(_('name parameter '
                    'requires a string as the value. {0}').format(type(name)))
        if not (type(resource) is str or type(resource) is unicode):
            raise ResourceServerIllegalParameterError(_('resource parameter '
                    'requires a string as the value. {0}').format(
                    type(resource)))
        if type(exclusive) is not bool:
            raise ResourceServerIllegalParameterError(_('exclusive parameter '
                    'must be a boolean value and not: {0}').format(
                    type(exclusive)))

        cmd, answ = self.client.send(Client.SJSON, 'release',
                {'name': name, 'resource_name': resource,
                'exclusive': exclusive})
        if answ['status'] == SUCCESS:
            return answ['resource']
        raise ResourceServerRemoteError("[{0}]: {1}".format(cmd,
                answ['message']))
