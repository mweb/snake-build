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
''' The file provides some common functions for all client command handlers.
'''

from snakebuild.resourceclient.servercmds import ResourceServer


def get_resource_server(config):
    ''' get an instance of the resource server.

        @param config: The config object to use for the required parameters.
    '''
    return ResourceServer(config.get_s('resourceclient', 'hostname'),
            config.get_s('resourceclient', 'port'))
