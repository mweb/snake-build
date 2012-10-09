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
import json
import logging

from snakebuild.i18n import _

LOG = logging.getLogger('snakebuild.resourceserver.resource')


class ResourceException(BaseException):
    ''' This exception gets thrown if the resourcemanager or a resource has
        a problem during the normal usage.
    '''


def init_resource_from_string(obj_str):
    ''' This function creates a new resource object from a string which
        contains a valid json string with the following structure:

        { "name": "TEResource",
          "parallel_count": 1,
          "keywords": ["test", "build", "melt"],
          "parameters": { "ip": "192.168.1.92" }
        }

        The name must be a unique name for all the currently instancieted
        resources otherwise this resource can not be managed by the resource
        manager.
        The parallel_count must be an integer that indicates how man user might
        acquire this resource at once.

        The keywords entry must be a list with all the keywords that this
        resource server should be usable. A client usually dosn't ask for a
        specific resource instead it asks for a type (keyword).

        The parameters must be a dictionary with an arbitrary structure (only
        basic types) this structure will be accessible from a client to be able
        to use the resource.

        @param obj_str: The json string to parse
        @return: The new Resource object
    '''
    obj = json.loads(obj_str)
    return init_resource_from_obj(obj)


def init_resource_from_obj(obj):
    ''' This function creates a new resource object from a dictionary structure
        which must be somethin similar to this.

        { "name": "TEResource",
          "parallel_count": 1,
          "keywords": ["test", "build", "melt"],
          "parameters": { "ip": "192.168.1.92" }
        }

        The name must be a unique name for all the currently instancieted
        resources otherwise this resource can not be managed by the resource
        manager.
        The parallel_count must be an integer that indicates how man user might
        acquire this resource at once.

        The keywords entry must be a list with all the keywords that this
        resource server should be usable. A client usually dosn't ask for a
        specific resource instead it asks for a type (keyword).

        The parameters must be a dictionary with an arbitrary structure (only
        basic types) this structure will be accessible from a client to be able
        to use the resource.

        @param obj_str: The json string to parse
        @return: The new Resource object
    '''
    if not ('name' in obj and 'parallel_count' in obj and
            'keywords' in obj and 'parameters' in obj):
        raise ResourceException('Not all requiered keys available.')

    if type(obj['name']) in (str, unicode):
        resource = Resource(obj['name'])
    else:
        raise ResourceException(_('The name type must be a string. Got: '
                '{0}').format(obj['name']))
    if type(obj['keywords']) is list:
        for key in obj['keywords']:
            if type(key) in (str, unicode):
                if key.lower() in resource.keywords:
                    LOG.warning(_('Duplicated keywords ({0}) for resource '
                            '({0})').format(key, resource.name))
                else:
                    resource.keywords.append(key.lower())
    if type(obj['parallel_count']) is int:
        resource.parallel_count = obj['parallel_count']
    else:
        try:
            resource.parallel_count = int(obj['parallel_count'])
        except ValueError:
            raise ResourceException(_('The parallel_count is not an int value:'
                    ' {0}').format(obj['parallel_count']))

    if type(obj['parameters']) is dict:
        resource.parameters = obj['parameters']
    else:
        raise ResourceException(_('The parameters is not of type dict: '
                '{0}').format(obj['parameters']))

    return resource


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
        self.exclusive = False
        # if set then the server is shutting down and no new client should get
        # the resource
        self.run = True

        # the current user names of this resource
        self.users = []

        # the counter variables
        self._parallel_count = 1
        self._current_count = 1

        # the parameters and the keywords
        self.parameters = {}
        self.keywords = [name.lower()]

    @property
    def parallel_count(self):
        ''' The number of parallel runs that the instance of this resource
            can run.
        '''
        return self._parallel_count

    @parallel_count.setter
    def parallel_count(self, value):
        ''' The setter method for the parallel count value. take care if the
            current count must be increased as well or not.

            @param value: The new value to set
        '''
        if type(value) is not int:
            raise ResourceException(_('Wrong type for parallel_count must '
                    'be an integer. Got: {0} ({1})').format(value,
                    type(value)))

        if value <= 0:
            raise ResourceException(_('Illegal value for parallel count must '
                    'be >0. Got: {0:d}').format(value))
            self._parallel_count = value

        self.count_lock.acquire()
        # if no resource are in use then set the current count to the same
        # value
        if self._current_count == self._parallel_count:
            self._current_count = value
        elif self.exclusive:
            pass
        else:
            self._current_count = value -\
                    (self._parallel_count - self._current_count)

        self._parallel_count = value
        self.count_lock.release()

    @property
    def current_count(self):
        ''' The counter used to see how many resources are free to be used. '''
        return self._current_count

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
        while self.run:
            self.count_lock.acquire()
            if (self._current_count <= 0 or
                    (self.wait_for_exclusive and not exclusive) or
                    (exclusive and
                        self._current_count != self._parallel_count)):
                # there are no free slots available or there is some one
                # waiting to get it for exclusive usage therfore all others
                # have to wait till it is theyr turn.
                if block:
                    self.release_listener.clear()
                    if exclusive:
                        self.wait_for_exclusive = True
                    self.count_lock.release()
                    self.release_listener.wait()
                    continue
                else:
                    self.count_lock.release()
                    return False

            if exclusive:
                self._current_count = 0
                self.wait_for_exclusive = False
                self.exclusive = True
            else:
                self._current_count -= 1

            self.users.append(uname)
            self.count_lock.release()

            return True

        return False

    def release(self, uname, exclusive):
        ''' Release the resource, if the resource was locked by the given user
            before.

            @param uname: The user name that acquired the resource before
            @param exclusive: If this boolean is set to True then the resource
                    which must be blocked exclusive will only release the
                    exclusive lock but will keep one lock for the given user.

            @return: True if release worked. Otherwise a ResourceException is
                    raised
        '''
        self.count_lock.acquire()
        if not uname in self.users:
            LOG.error(_("A user ({0}) tried to release a resource which he "
                    "didn't acquire before.").format(uname))
            self.count_lock.release()
            raise ResourceException(_("Tried to release resource with the "
                    'wrong user: {0}').format(uname))

        if exclusive:
            if not self.exclusive:
                LOG.error(_("A user ({0}) tried to free exclusive usage only "
                        "for a resource which is not acquired "
                        "exclusively.").format(uname))
                self.count_lock.release()
                raise ResourceException(_('Resource not acquired exclusively '
                        'before.'))
            self._current_count = self._parallel_count - 1
            self.exclusive = False
            self.count_lock.release()
            self.release_listener.set()
            return True

        self.users.remove(uname)
        if self.exclusive:
            self._current_count = self._parallel_count
            self.exclusive = False
        else:
            self._current_count += 1
        self.count_lock.release()
        self.release_listener.set()
        return True

    def do_shutdown(self):
        ''' Prepare the resource for shutdown. All new request will be
            rejected.
        '''
        self.run = False
        LOG.info(_("Received shutdown signal. Currently used resources: "
                "{0}").format(self._parallel_count - self._current_count))
        self.release_listener.set()
