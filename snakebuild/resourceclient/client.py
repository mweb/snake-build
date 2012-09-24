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
''' This is the main entry for the resource client command line tool.
'''

from snakebuild.common import output
from snakebuild.commands import handle_cmd
from snakebuild.i18n import _

from snakebuild.resourceclient.clientcmds import *


def run_client(args, config):
    ''' Start the client command and see what the user wants.

        @param args: the arguments given to the command.
        @param config: The loaded config object
        @return true or false depends on success or failure
    '''
    if args.username is not None:
        config.set('ResourceClient', 'clientname', args.username)
    if args.server is not None:
        config.set('ResourceClient', 'hostname', args.server)
    if args.port is not None:
        config.set('ResourceClient', 'port', args.port)

    try:
        return handle_cmd(args, config)
    except KeyboardInterrupt:
        output.error(_('Abort by Keyboard Interrupt.'))
        return False
