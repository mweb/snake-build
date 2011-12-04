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
''' This files contains the dictionary with all the commands that the resrouce
    server supports via the network connection.
'''

import logging

from snakebuild.communication.commandstructure import prepare_answer, \
        prepare_error

LOG = logging.getLogger('snakebuild.resourcesserver.commands')


def _status_list(cmd, res_mgr):
    ''' This command returns a list with all the configured resources. In
        addtion to the name we return the current status and the keywords
        of all the resources.

        @param cmd: The command that lead to the call of this function
        @param res_mgr: The resource manager instance
        @return: the answer object to return to the client
    '''
    if cmd != 'status_list':
        LOG.error('_status_list called with the wrong command: %s' % cmd)
        return prepare_error('Server Error')

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


def _resource_details(cmd, res_mgr, name):
    ''' This command returns all the configured information about a resouce.
        The data sent is similar to the data available within the config file.
        Just the run time datas are added, like free slots and current users.

        @param cmd: The command that lead to the call of this function
        @param res_mgr: The resource manager instance
        @param name: The name of the resource to get the details for
        @return: the answer object to return to the client
    '''
    if cmd != 'resource_details':
        LOG.error('_resource_details called with the wrong command: %s' % cmd)
        return prepare_error('Server Error')

    if not(type(name) == str or type(name) == unicode):
        return prepare_error('Illegal value for the name. Expected a string '
                'but got {0}'.format(type(name)))

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
        return prepare_error('The expected resource does not exist: '
                '{0}'.format(name))


def _shutdown(cmd, res_mgr):
    ''' This method is called on a shutdown request.

        @param cmd: The called command.
        @param res_mgr: The ResourceManager instance
    '''
    if cmd != 'shutdown':
        LOG.error('_status_list called with the wrong command: %s' % cmd)
        return prepare_error('Server Error')

    res_mgr.shutdown()

    return prepare_answer()


# The commands for the message handler
COMMANDS = {'status_list': (_status_list, 'Get a simple list with all the '
                'resources available. This includes the current status.', [],
                {}, False),
            'resource_details': (_resource_details, 'Get the full information '
                'about a resource.', ['name'], {'name': 'The name of the '
                'resource to get the information from.'}, False),
            'shutdown': (_shutdown, 'Shutdown the server', [], {}, True)}
