# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2012 Mathias Weber <mathew.weber@gmail.com>
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
''' The package for a simple web based resourceviewer. To see all the
    currently configured resources and its current state.
'''

from snakebuild.i18n import _
from snakebuild.common import Daemon
from snakebuild.resourceviewer.webserver import WebServer


def start_webserver(options, arguments, config):
    ''' Start the resource viewer webserver.

        @param options: the options set vie the command line parameters
        @param config: the global configuration to use to start the server
        @param arguments: the arguments for the command.
        @return true or false depending on success or failure
    '''
    if not len(arguments) == 1:
        print(_("Could not start the webserver since the starting command is "
                "not supported expected one argument but got: {0:d}").format(
                len(arguments)))
        return False

    cmd = arguments[0].lower()

    if cmd == 'stop':
        Daemon(WebServer(config), Daemon.STOP)
    elif cmd == 'start':
        if options.background:
            Daemon(WebServer(config), Daemon.START)
        else:
            Daemon(WebServer(config), Daemon.FOREGROUND)
    elif cmd == 'browser':
        pass
    else:
        print(_("The given command is not supported by the resourceviewer "
                "server: {0}").format(cmd))
        return False
