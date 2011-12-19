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

from snakebuild.common import output
from snakebuild.communication import ClientCommunicationException
from snakebuild.commands import command
from snakebuild.resourceclient.clientcmds.common import get_resource_server
from snakebuild.resourceclient.servercmds import ResourceServerRemoteError

@command('details')
def details(options, config, name):
    ''' Get the details about one resource.

        @param options: The options provided to this command call
        @param config: The config object to use
        @param name: The name of the resource to get the details for

        @return True on success, False on error and nothing on wrong usage.
    '''
    srvr = get_resource_server(config)
    try:
        answer = srvr.get_resource_details(name)
    except ResourceServerRemoteError, exc:
        output.error("Got error while talking with the server:\n "
                "{0}".format(exc))
        return False
    except ClientCommunicationException, exc:
        output.error(exc)
        return False

    print "Resource: {0[name]}".format(answer)
    print "Slots/Free: {0[slots]}/{0[free]}".format(answer)
    print "Users: {0}".format(", ".join(answer['users']))
    print "Keywords: {0}".format(", ".join(answer['keywords']))
    print "Parameters:"

    return True
