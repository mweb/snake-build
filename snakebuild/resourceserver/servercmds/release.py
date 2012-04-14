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
from snakebuild.communication.server import remote_command
from snakebuild.resourceserver.resource import ResourceException

LOG = logging.getLogger('snakebuild.resourcesserver.commands')


@remote_command('release', False)
def release(res_mgr, name, resource_name, exclusive=False):
    ''' This command releases a resource which where acquired before.

        The exclusive boolean is to release the exclusive lock from a
        resource. The user will keep a normal lock of the resource till he
        calls the release without the exclusive lock.
        If a resource is locked exclusive and this call is called without
        the exclusive lock then the resource will be released completely.

        @param res_mgr: The resource manager instance
        @param name: The name of the user to get this resource
        @param resourcre_name: The name of the resource to release
        @param exclusive: Sitch on/off the exclusive release of the lock
        @return: the answer object to return to the client
    '''
    try:
        res_mgr.release(resource_name, name, exclusive)
    except ResourceException, exc:
        return prepare_error(str(exc))

    answer = prepare_answer()
    answer['resource'] = resource_name

    return answer
