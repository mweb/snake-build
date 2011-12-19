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
''' The snakebuild.resourceserver.servercmd status_list. This command provides
    a quick overview over all the resources and its current status.
'''

import logging

from snakebuild.communication.commandstructure import prepare_answer, \
        prepare_error
from snakebuild.resourceserver.servercommands import command

LOG = logging.getLogger('snakebuild.resourcesserver.commands')


@command('acquire', False)
def acquire(res_mgr, name, tag, exclusive=False):
    ''' This command acquires a resource of the given tag. If the tag or
        resource doesn't exist it will return an error. This command might
        wait if no resource is available.

        @param res_mgr: The resource manager instance
        @param name: The name of the user to get this resource
        @param tag: The tag of the resource to get
        @param exclusive: Should the resource be acquired exclusivly True
            if yes
        @return: the answer object to return to the client
    '''
    resource = res_mgr.acquire(name, tag, exclusive)
    if resource is None:
        return prepare_error("No resource with the given tag ({0}) could be "
                "acquired.".format(tag))

    answer = prepare_answer()
    answer['resource'] = resource

    return answer
