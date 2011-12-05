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
''' The snakebuild.resourceserver.servercmd shutdown. This command provides
    the functionality to shutdown the resource server.
'''

import logging

from snakebuild.communication.commandstructure import prepare_answer, \
        prepare_error

LOG = logging.getLogger('snakebuild.resourcesserver.servercmds.shutdown')


def shutdown(cmd, res_mgr):
    ''' This method is called on a shutdown request.

        @param cmd: The called command.
        @param res_mgr: The ResourceManager instance
    '''
    if cmd != 'shutdown':
        LOG.error('_status_list called with the wrong command: %s' % cmd)
        return prepare_error('Server Error')

    res_mgr.shutdown()

    return prepare_answer()
