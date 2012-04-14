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
''' The snakebuild build agent run function to start a build agent. '''

import logging

from snakebuild.common import output
from snakebuild.common import Daemon
from snakebuild.i18n import _
from snakebuild.commands import command, handle_cmd
from snakebuild.communication import Server
# this needs to be imported to fill the REMOTE_COMMANDS
import snakebuild.buildagent.agentcmds
#from snakebuild.buildagent.buildagent import BuildAgent

LOG = logging.getLogger('snakebuild.buildagent.agent')


def run_agent(options, arguments, config):
    ''' Start the build agent.

        @param options: The parsed commandline options.
        @param config: The config object loaded during start.
        @param arguments: the arguments for the command.

        @return true or false depends on success or failure
    '''
    try:
        return handle_cmd(arguments, options, config)
    except KeyboardInterrupt:
        output.error(_('Abort by keyboard interrupt.'))
        return False


@command('stop')
def stop_agent(options, config, name="snakebuild"):
    ''' Stop the agent that is running in the background.

        @param options: The options provided to this command call
        @param config: The config object to use
        @param name: The name of the agent to stop.
        @return True on success, False on error and nothing on wrong usage.
    '''
    host = config.get_s('buildagent', 'hostname')
    port = config.get_s('buildagent', 'port')
    name = "ba_{0}".format(name.lower())

    Daemon(Server(host, port, name), Daemon.STOP)
    return True


@command('start')
def start_agent(options, config, name="SnakeBuild"):
    ''' Start the build agent.

        By specifing the name it is possible to run multiple build agent
        instances on one server.

        @param options: The options provided to this command call
        @param config: The config object to use
        @param name: The name to use for the build agent. This name has to be
                unique on one server.
        @return True on success, False on error and nothing on wrong usage.
    '''
    host = config.get_s('buildagent', 'hostname')
    port = config.get_s('buildagent', 'port')
    name = "ba_{0}".format(name.lower())

#    agent = BuildAgent()
    agent = None
    Daemon(Server(host, port, name, agent), Daemon.START)
    return True
