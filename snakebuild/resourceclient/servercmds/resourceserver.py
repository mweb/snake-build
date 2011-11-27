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
''' The following class ResourceServer provides access commands to communicate
    with the ResourceServer without the need to now the detailed commands.
'''

from snakebuild.communication.client import Client

class ResourceServer(object):
    '''
    '''

    def __init__(self, url, port):
        ''' Init the server object to communicate with the server later on

            @param url: The url of the server to connect to
            @param port: The network port where the server is listening.
        '''
        self.client = Client(url, port)
