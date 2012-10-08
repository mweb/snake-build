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


@command('release', (
    (('name',), {'help': _('The name of the resource to release')}),
    (('--exclusive',), {'action': 'store_true', 'help': _('Set this flag to '
            'release the exclusive flag from a resource and receive a '
            '"normal" lock'), 'default': False}),
    ))
def release(args, config):
    ''' Release a previsously acquired resource.

        @param args: The arguments provided to this command
        @param config: The config object to use

        @return True on success, False on error and nothing on wrong usage.
    '''
    srvr = get_resource_server(config)

    username = config.get_s('ResourceClient', 'clientname')

    try:
        answer = srvr.release_resource(username, args.name, args.exclusive)
    except ResourceServerRemoteError, exc:
        output.error(_("Got error while talking with the server:\n "
                "{0}").format(exc))
        return False
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    output.message(answer)
    return True
