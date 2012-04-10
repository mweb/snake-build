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


LOG = logging.getLogger('snakebuild.buildagent.agent')


def run_agent(options, arguments, config):
    ''' Start the build agent.

        @param options: The parsed commandline options.
        @param config: The config object loaded during start.
        @param arguments: the arguments for the command.

        @return true or false depends on success or failure
    '''
    return True
