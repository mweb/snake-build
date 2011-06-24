# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>


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
