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
''' The details command to request the details for one resource from the
    resource server.
'''

from snakebuild.i18n import _
from snakebuild.common import output
from snakebuild.communication import ClientCommunicationException
from snakebuild.remote.resourceserver import ResourceServerRemoteError
from snakebuild.resourceclient.clientcmds.common import get_resource_server
from snakebuild.resourceclient.commandlineparser import SHELL_COMMANDS, command


@command('details', (
    (('name',), {'help': _('The name of the resource to get the details '
            'for')}),
    ))
def details(args, config):
    ''' Get the details about one resource.

        @param args: The arguments provided with the command
        @param config: The config object to use

        @return True on success, False on error and nothing on wrong usage.
    '''
    srvr = get_resource_server(config)
    try:
        answer = srvr.get_resource_details(args.name)
    except ResourceServerRemoteError, exc:
        output.error(_("Got error while talking with the server:\n "
                "{0}").format(exc))
        return False
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    print _("Resource: {0[name]})").format(answer)
    print _("Slots/Free: {0[slots]}/{0[free]}").format(answer)
    print _("Users: {0}").format(", ".join(answer['users']))
    print _("Keywords: {0}").format(", ".join(answer['keywords']))
    print _("Parameters:")

    return True
