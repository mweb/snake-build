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
''' This file provides a start_server method to start the ResourceServer.
'''

from snakebuild.common import Daemon
from snakebuild.communication import Server
from snakebuild.resourceserver.commands import COMMANDS
from snakebuild.resourceserver.resource import ResourceManager


def start_server(options, arguments, config):
    ''' Start the resource server.

        @param options: the options set via the command line parameters
        @param config: the global configuration to use for starting the server
        @param arguments: the arguments for the command the first argument
                within this list is always the command it self.
        @return true or false depends on success or failure
    '''
    stop = False
    if not (len(arguments) == 0 or len(arguments) == 1):
        print "Could not start the resource server illeagel arguments."
        return False

    if len(arguments) == 1:
        cmd = arguments[0].lower()
        if cmd == 'stop':
            stop = True
        elif cmd == 'start':
            stop = False
        else:
            print "Command not supported for starting: %s" % arguments[0]

    host = config.get_s('resourceserver', 'hostname')
    port = config.get_s('resourceserver', 'port')
    name = 'resourceserver'

    if stop:
        Daemon(Server(host, port, COMMANDS, name), Daemon.STOP)
    else:
        resourcemanager = ResourceManager(config.get_s('resourceserver',
               'resources_directory'))
        if options.foreground:
            Daemon(Server(host, port, COMMANDS, name, resourcemanager),
                    Daemon.FOREGROUND)
        else:
            Daemon(Server(host, port, COMMANDS, name, resourcemanager),
                    Daemon.START)

    return True
