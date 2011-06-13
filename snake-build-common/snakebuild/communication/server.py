# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>


class ServerCommunicationException(BaseException):
    ''' The exception that gets trown on an error during the communication with
        the client.
    '''


class Server(object):
    ''' This class is simple wrapper class for a server class which handles
        sjson messages. The parsing of the messages is done. The class must
        only provide a list with commands and the commands to call on this
        commands.

        # TODO
        Message Types:

        sjson
        -----
        Identifier byte = 'a' or 0x61
          | |    | ... |
           |   |    \----> The data bytes as a json string (must be complete)
           |   |           the length must comply with the length given in the
           |   |           length field.
           |   \---------> The length field (4 bytes) specifying the length of
           |               the message. Must be encoded as big-endian.
           \-------------> The idenifier byte (must be 'a' or as value 0x61)

        The data type to provide for sending a SJSON request must be a
        dictionary/list or other basic type that can be transformed to a json
        string without special handling. The answer for a sjson message is
        a dictionary/list or other basic type as well.

        No other types are currently supported but others might follow.
    '''
    # this defines the known message types
    SJSON, UNKNWON = range(2)

    def __init__(self, host, port):
        ''' Create a server object with the given host and port. The server
            does not start listening until the run method is called.

            @param host: The host address (as a string)
            @param port: The network port to use for the connection (as int)
        '''
        self.host = host
        self.port = port
