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
''' The file contains the Resource object which handles the access to a
    Resource.
'''

import threading


class ResourceException(BaseException):
    ''' The exception that gets thrown if an error within the Resource object
        gets thrown.
    '''


class Resource(object):
    ''' This class provides the methods to acquire and release a resource.
        The calls to this methods must be synchronized so that they can be
        called from multiple threads.
    '''
    def __init__(self, name):
        ''' The constructor of the object

            @param name: The name of the resource to create
        '''
        self.name = name

        # control variables to synchronize access to this object
        self.count_lock = threading.Lock()
        self.release_listener = threading.Event()
        # if set then a client waits for exclusive usage
        self.wait_for_exclusive = False
        # if set then the server is shutting down and no new client should get
        # the resource
        self.run = True

        # the current user names of this resource
        self.users = []

        # the counter variables
        self.parallel_count = 1
        self.current_count = 1

        # the parameters and the keywords
        self.parameters = {}
        self.keywords = [name]

    def acquire(self, uname, exclusive, block):
        ''' Acquire the resource if available otherwise this method blocks
            until the resource gets free to be used or the server gets a shut
            down request.

            @param uname: The user name to get the resource for
            @param exclusive: This boolean defines if the resource should be
                    acquired exclusive or normaly.
            @param blocks: This boolean defines if the call should block or if
                    it should return with no resource if not available.

            @return: True if acquire worked and False if not
        '''
        pass

    def release(self, uname, exclusive):
        ''' Release the resource, if the resource was locked by the given user
            before.

            @param uname: The user name that acquired the resource before
            @param exclusive: This boolean defines if the resource was acquired
                    exclusive or normaly.

            @return: True if release worked and False if not (usually resource
                    was not locked before by this user)
        '''
        pass

    def do_shutdown(self):
        ''' Prepare the resource for shutdown. All new request will be
            rejected.
        '''
        pass

    def set_parameters(self, params):
        ''' Set the parameters for the resource. This parameters will be
            accessible by a requester and should help to identify or access a
            resource.
            The param dictionary might be a nested dictionary.

            @param params: The params dictionary with all the key value pairs
        '''
        if params is dict:
            self.parameters = params
        else:
            raise ResourceException('params object is not a dictionary')
