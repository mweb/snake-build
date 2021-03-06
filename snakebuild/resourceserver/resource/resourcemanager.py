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
''' The file contains a class which is used as the resource manager. This
    instance will hold all the resources to be managed and will handle the
    scheduling of request to the different resources to have a good usage.
'''

import threading
import os.path
import logging
import json

from snakebuild.i18n import _
from snakebuild.common.versioneddir import VersionedDirBase
from snakebuild.resourceserver.resource import init_resource_from_obj
from snakebuild.resourceserver.resource import ResourceException

LOG = logging.getLogger('snakebuild.resourceserver.resource.resourcemanager')


class ResourceManager(object):
    ''' The resource manager class. This class manages a list of resources. An
        instance of this class will handle all the request for resources. This
        includes getting a new resource or releasing a resource. In addition
        it provides an interface to get information about the resources.
    '''

    def __init__(self, resource_repo):
        ''' Constructor. Create the ResourceManager object and load the
            resources from the configured resource directory.

            The resources are configured with a file for each resource. All the
            files must be stored within one directory. All files except the one
            starting with a dot (hidden files) or files ending with .bkp are
            read and interpreted as a resource.

            @param resource_repo: The resource repository to load and change.
        '''
        LOG.debug(_('Initialize ResourceManager'))
        self.resources = {}
        self.release_listener = threading.Event()
        self.keywords = {}
        self.run = True

        if not isinstance(resource_repo, VersionedDirBase):
            raise ResourceException('The resource location is not a versioned '
                    'directory. ResourceManager could not be created.')
        self.resources_respository = resource_repo
        self._load_resources()

        for name, resource in self.resources.iteritems():
            for keyword in resource.keywords:
                if keyword in self.keywords:
                    if name in self.keywords[keyword]:
                        # it is already here why?
                        LOG.warning(_('A dupplicate keyword, resource name, '
                                'this should not happen. Ignore it: '
                                'Keyword={0}, ResoruceName={1}').format(
                                keyword, name))
                        continue
                    self.keywords[keyword].append(name)
                else:
                    self.keywords[keyword] = [name]

    def shutdown(self):
        ''' Shut down the resource manager. If there are any request waiting
            wake up the given thread and decline all questions for resources.
        '''
        LOG.info(_('Received shutdown signal.'))
        self.run = False
        self.release_listener.set()
        for resource in self.resources.itervalues():
            resource.do_shutdown()

    def acquire(self, uname, keyword, exclusive):
        ''' Acquire a resource. This will return the resource acquired. This
            method will block if no resource for the given keyword is
            available.

            @param uname: The user name to use as the user of the resource
            @param keyword: The keyword to search for the resource
            @param exclusive: Boolean value if set to True then the user will
                use the resource exclusive no one else should be using it.

            @return: The name of the resource acquired or None if not available.
        '''
        keyword = keyword.lower()
        if not keyword in self.keywords:
            LOG.warning(_('The user ({0}) tried to access a resource with the '
                    'keyword "{1}". But this keyword does not exist.').format(
                    uname, keyword))
            return None

        while self.run:
            names = self.keywords[keyword]
            self.release_listener.clear()
            for name in names:
                if self.resources[name].acquire(uname, exclusive, False):
                    return name
            self.release_listener.wait()

    def release(self, resourcename, uname, exclusive):
        ''' Release a given resource. If the resource wasn't locked by the
            given user nothing will happen.

            The exclusive boolean is to release the exclusive lock from a
            resource. The user will keep a normal lock of the resource till he
            calls the release without the exclusive lock.
            If a resource is locked exclusive and this call is called without
            the exclusive lock then the resource will be released completely.

            @param resourcename: The name of the resource to release
            @param uname: The user name how owns the lock
            @param exclusive: Switch on/off the exclusive release of the lock

            @return: True if released and otherwise a ResoruceException is
                    raised
        '''
        if not resourcename in self.resources:
            LOG.error(_('Release command called for a not existing resource '
                    '{0} User: {1}').format(resourcename, uname))
            raise ResourceException(_('Release command called for a not '
                    'existing resource {0} User: {1}').format(resourcename,
                    uname))

        self.resources[resourcename].release(uname, exclusive)
        self.release_listener.set()
        return True

    def _load_resources(self):
        ''' Load all the resources from the given directory.

            @param dirname: The full path to the resource to load
        '''
        LOG.info(_('Loading resources from: {0}').format(
                self.resources_respository.path))
        for element in os.listdir(self.resources_respository.path):
            if element.startswith('.') or element.endswith('bkp'):
                # ignore hidden files
                continue
            if os.path.isfile(self.resources_respository.get_full_path(
                    element)):
                self._load_resource(self.resources_respository.get_full_path(
                        element))

    def _load_resource(self, filename):
        ''' Load the given resource from the given file.

            @param filename: The name of the file (full path)
        '''
        LOG.debug(_('Load resource from file: {0}').format(filename))
        resource_desc = json.load(open(filename, 'r'))
        resource = init_resource_from_obj(resource_desc)
        if resource is not None:
            if resource.name in self.resources:
                LOG.warning(_('A resource with name "{0}" already exists. '
                        'Ignore it. Filename: {1}').format(resource.name,
                        filename))
                return
            self.resources[resource.name] = resource
        else:
            LOG.error(_('Could not load resource from given file: '
                    '{0}').format(filename))
