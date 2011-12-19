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

from snakebuild.communication.commandstructure import prepare_answer
from snakebuild.resourceserver.servercommands import command

LOG = logging.getLogger('snakebuild.resourcesserver.commands')


@command('status_list', False)
def status_list(res_mgr):
    ''' This command returns a list with all the configured resources. In
        addtion to the name we return the current status and the keywords
        of all the resources.

        @param res_mgr: The resource manager instance
        @return: the answer object to return to the client
    '''
    answer = prepare_answer()
    answer['resources'] = []
    for res in res_mgr.resources.itervalues():
        values = {'name': res.name,
                'keywords': res.keywords,
                'slots': res.parallel_count,
                'free': res.current_count,
                'users': res.users}
        answer['resources'].append(values)

    return answer
