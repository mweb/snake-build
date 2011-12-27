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
''' The snakebuild.resourceserver.servercmd resource_details. This command
    provides access to the detail information of a resource.
'''

import logging

from snakebuild.i18n import _
from snakebuild.communication.commandstructure import prepare_answer, \
        prepare_error
from snakebuild.resourceserver.servercommands import command

LOG = logging.getLogger('snakebuild.resourcesserver.commands')


@command('resource_details', False)
def resource_details(res_mgr, name):
    ''' This command returns all the configured information about a resouce.
        The data sent is similar to the data available within the config file.
        Just the run time datas are added, like free slots and current users.

        @param res_mgr: The resource manager instance
        @param name: The name of the resource to get the details for
        @return: the answer object to return to the client
    '''
    if not(type(name) == str or type(name) == unicode):
        return prepare_error(_('Illegal value for the name. Expected a string '
                'but got {0}').format(type(name)))

    answer = prepare_answer()
    if name in res_mgr.resources:
        res = res_mgr.resources[name]
        values = {'name': res.name,
                'keywords': res.keywords,
                'slots': res.parallel_count,
                'free': res.current_count,
                'users': res.users,
                'parameters': res.parameters}
        answer = prepare_answer()
        answer['resource'] = values
        return answer
    else:
        return prepare_error(_('The expected resource does not exist: '
                '{0}').format(name))
