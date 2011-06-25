# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

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
