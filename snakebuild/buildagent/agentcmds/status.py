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
''' The snakebuild build agent remote command status. This command... '''

import logging

from snakebuild.i18n import _
from snakebuild.communication.commandstructure import prepare_answer, \
        prepare_error
from snakebuild.communication.server import remote_command

LOG = logging.getLogger('snakebuild.buildagent.commands')


@remote_command('status', False)
def status(buildagent):
    ''' This command returns the current status of this build agent. 

        @param buildagent: The buildagent instance
        @return: The answer object to return to the client
    '''
    answer = prepare_answer()
    LOG.error(_('NOT YET IMPLEMENTED'))
    return answer
