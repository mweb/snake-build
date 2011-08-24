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
''' This file provides some common helper functions for the server and client.
'''

import json


def prepare_sjson_data(msg):
    ''' Prepare the data for a sjson request.

        @param msg: The dictionary/list or basic type to transfer to the
                server as a json string.
        @return: the message as a string including the header.
    '''
    message = json.dumps(msg)
    length = len(message)
    data = ('a' + chr((length >> 24) % 256) + chr((length >> 16) % 256) +
            chr((length >> 8) % 256) + chr(length % 256))

    data += message
    return data
