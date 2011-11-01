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

from snakebuild.common import Config
from snakebuild.resourceserver.resource import init_resource_from_obj

LOG = logging.getLogger('snakebuild.resourceserver.resource.resourcemanager')


class ResourceManager(object):
    ''' The resourcemanager class. This class manages a list of resources. An
        instance of this class will handle all the request for resources. This
        includes getting a new resource or releaseing a resource. In addition
        it provides an interface to get informations about the resources.
    '''

    def __init__(self):
        ''' Constructor. Create the ResourceManager object and load the
            resources from the configured resource directory.
        '''
        LOG.debug('Initialize ResourceManager')
        dirname = Config().get_s('resourceserver', 'resource_config_dir')
        self.resources = {}
        self.release_listener = threading.Event()
        self.keywords = {}
        self.run = True

        if os.path.isdir(dirname):
            self._load_resources(dirname)

        # TODO initialize the keywords list

    def shutdown(self):
        ''' Shut down the resource manager. If there are any request waiting
            wake up the given thread and decline all questions for resources.
        '''
        pass

    def _load_resources(self, dirname):
        ''' Load all the resources from the given directory.

            @param dirname: The full path to the resource to load
        '''
        LOG.info('Loading resources from: %s' % dirname)
        for element in os.listdir(dirname):
            if element.startswith('.') or element.endswith('bkp'):
                # ignore hidden files
                continue
            if os.path.isfile(os.path.join(dirname, element)):
                self._load_resource(os.path.join(dirname, element))

    def _load_resource(self, filename):
        ''' Load the given resource from the given file.

            @param filename: The name of the file (full path)
        '''
        LOG.debug('Load resource from file: %s' % filename)
        resource_desc = json.load(open(filename, 'r'))
        resource = init_resource_from_obj(resource_desc)
        if resource is not None:
            if resource.name in self.resources:
                LOG.warning('A resource with name "%s" already exists. Ignore '
                        'it. Filename: %s' % (resource.name, filename))
                return
            self.resources[resource.name] = resource
        else:
            LOG.error('Could not load resource from given file: %s' % filename)
