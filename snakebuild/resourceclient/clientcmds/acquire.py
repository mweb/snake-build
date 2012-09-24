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
from snakebuild.commands import command
from snakebuild.resourceclient.clientcmds.common import get_resource_server
from snakebuild.remote.resourceserver import ResourceServerRemoteError


@command('acquire', (
    (('--exclusive',), {'action': 'store_true', 'help': _('Set this flag to '
            'get a resource fro exclusive usage.'), 'default': False}),
    (('tag',), {'help': _('The tag to search for in a resource or a resource '
            'name.')})
    ))
def acquire(args, config):
    ''' Acquire a resource with a given tag. The tag is either a tag defined
        by one or multiple resources or a name of a resource to get.

        @param args: The arguments provided to this command
        @param config: The config object to use

        @return True on success, False on error and nothing on wrong usage.
    '''
    srvr = get_resource_server(config)

    name = config.get_s('ResourceClient', 'clientname')

    try:
        answer = srvr.acquire_resource(name, args.tag, args.exclusive)
    except ResourceServerRemoteError, exc:
        output.error(_("Got error while talking with the server:\n "
                "{0}").format(exc))
        return False
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    output.message(answer)
    return True
