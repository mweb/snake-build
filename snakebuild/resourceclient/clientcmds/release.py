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
from snakebuild.resourceclient.servercmds import ResourceServerRemoteError


@command('release')
def release(options, config, name, exclusive=False):
    ''' Release a previsously acquired resource.

        @param options: The options provided to this command call
        @param config: The config object to use
        @param name: The name of the resource to release.
        @param exclusive: Set this flag to True to release the exclusive usage
            of a resource but keep one "normal" lock of the resource.

        @return True on success, False on error and nothing on wrong usage.
    '''
    srvr = get_resource_server(config)

    username = config.get_s('ResourceClient', 'clientname')
    if options.username is not None:
        username = options.username

    if type(exclusive) is not bool:
        if type(exclusive) is str or type(exclusive) is unicode:
            if exclusive.lower() == "true" or exclusive.lower() == "exclusive":
                exclusive = True
            elif exclusive.lower() == "false":
                exclusive = False
            else:
                output.error(_("The value for the exclusive flag has to be "
                        "either true, exclusive or false, everything else is "
                        "invalid."))
                return False
        else:
            output.error(_("The given value for the exclusive flag could not "
                    "be parsed"))
            return False

    try:
        answer = srvr.release_resource(username, name, exclusive)
    except ResourceServerRemoteError, exc:
        output.error(_("Got error while talking with the server:\n "
                "{0}").format(exc))
        return False
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    output.message(answer)
    return True
