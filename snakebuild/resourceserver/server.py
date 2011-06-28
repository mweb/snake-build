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

from snakebuild.common import Daemon
from snakebuild.resourceserver import ResourceServer

def start_server(options,  arguments):
    ''' Start the resource server.

        @param options: the options set via the command line parameters
        @param arguments: the arguments for the command the first argument
                within this list is always the command it self.
        @return true or false depends on success or failure
    '''
    if not len(arguments) == 0:
        # TODO
        return False

    if options.foreground:
        Daemon(ResourceServer(), Daemon.FOREGROUND)
    elif options.stop:
        Daemon(ResourceServer(), Daemon.STOP)
    else:
        Daemon(ResourceServer(), Daemon.START)
    try:
        print "START HERE"
    except KeyboardInterrupt:
        print('Abort by Keyboard Interrupt.')
        return False
