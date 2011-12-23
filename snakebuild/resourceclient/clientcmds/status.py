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
''' The status command for getting the status of all resources on a resource
    server.
'''

from snakebuild.i18n import _
from snakebuild.common import output
from snakebuild.commands import command
from snakebuild.communication import ClientCommunicationException
from snakebuild.resourceclient.clientcmds.common import get_resource_server
from snakebuild.resourceclient.servercmds import ResourceServerRemoteError


@command('status')
def status(options, config):
    ''' This is the command to get a list with information about all the
        resources.

        @param options: The options provided to this command call
        @param config: The config object to use.

        @return True on success, False on error and nothing on wrong usage.
    '''
    srvr = get_resource_server(config)
    try:
        answer = srvr.get_status_list()
    except ResourceServerRemoteError, exc:
        output.error(_("Got error while talking with the server:\n "
                "{0}").format(exc))
        return False
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    print _("Name            | Slots/Free | Users")
    for resource in answer:
        print _("{0[name]:<15s} |  {0[slots]:>4d}/{0[free]:<4d} | {1}").format(
            resource, ", ".join(resource['users']))
    return True
