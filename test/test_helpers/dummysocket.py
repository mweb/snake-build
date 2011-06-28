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


class DummySocket(object):
    ''' This socket implements the socket methods to offer simple testing of
        methods which require an open socket.
        With this no real socket is needed and the content of the messages can
        be controlled.

        Currently only the recv message is supported others will follow.
    '''
    def __init__(self):
        ''' Initialize the DummySocket no data will be stored for now.
        '''
        self.data = ""

    def add_data(self, msg):
        ''' Add the given string to the current data for receiving with the
            recv method.

            @param msg: The message as a string to add
        '''
        self.data += msg

    def recv(self, length):
        ''' This method simulates the recv method from the socket class. It
            does return the number of bytes from the current data string. If
            not enough bytes are available it will return as many as it has.

            @param length: The max lenght of the data to receive
            @return: The message as string
        '''
        msg = self.data[:length]
        self.data = self.data[length:]
        return msg

    def close(self):
        ''' Simulate the close method of the socket. Clear the data buffer. '''
        self.data = ''
