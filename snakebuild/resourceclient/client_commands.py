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
''' This files contains the dictionary with all the commands which are
    supported by the resource client command.
'''

from snakebuild.common import output
from snakebuild.communication import ClientCommunicationException
from snakebuild.resourceclient.servercmds import ResourceServer, \
        ResourceServerRemoteError


def _status(cmd, options, config):
    ''' This is the command to get a list with information about all the
        resources.

        @param cmd: The command string that lead to this call
        @param options: The options provided to this command call
        @param config: The config object to use.
    '''
    if cmd != 'status':
        output.error('Status called with a wrong command: "{0}"'.format(cmd))
        return

    srvr = ResourceServer(config.get_s('resourceclient', 'hostname'),
            config.get_s('resourceclient', 'port'))
    try:
        answer = srvr.get_status_list()
    except ResourceServerRemoteError, exc:
        output.error("Got error while talking with the server:\n "
                "{0}".format(exc))
        return
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    print "Name            | Slots/Free | Keywords"
    for resource in answer:
        print ("{0[name]:<15s} |  {0[slots]:>4d}/{0[free]:<4d} | {1}".format(
            resource, ", ".join(resource['keywords'])))
    return True


COMMANDS = {'status': (_status, 'Get the status of all configured resources.',
            [], {})}
