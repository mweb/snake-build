# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import socket
import json


class ClientCommunicationException(BaseException):
    ''' The exception that gets trown on an error during the communication with
        the server.
    '''


class Client(object):
    ''' This class is simple wrapper class for communication with a server.
        The message send and receive implmented within this class is a simple
        protocoll where the first byte sent defines the type of the message
        currently only one type is supported.
        The communication is always with a TCP/IP socket. Nothing else is
        curently supported.

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
        ''' Create a client with the given host address and network port
            to connect to. The connection will not be used until a messages
            is sent.

            @param host: The host address (as a string)
            @param port: The network port to use for the connection (as int)
        '''
        self.host = host
        self.port = port

    def send(self, mtype, msg, no_answer=False):
        ''' Send a message to the server ans try to receive an answer if this
            isn't disabled. The message type must be specified and the message
            data must be provided as the expected type for the given type.

            @param mtype: The type of the message to send. Use the defined
                types of this class (SJSON)
            @param msg: The message to send. Must be of the right type for
                    the given message type (SJSON for example takes a
                    dictionary which can be transformed to json).
            @param no_answer: If set to true no answer expected so don't wait
                    for it.

            @return: The answer from the server as a touple (type, answer) The
                    type specifies the answer type and the answer is the
                    rest of the message as a string.
        '''
        if mtype >= UNKNWON:
            raise ClientCommunicationException('The given message type is not '
                    'supported.')

        if mtype == SJSON:
            data = self._prepare_sjson_data(msg)
#        elif mytype == OTHER:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((self.host, self.port))
        sock.send(data)

        if no_answer:
            sock.close()
            return (None, None)
        try:
            result = self._receive(sock)
        except KeyboardInterrupt, x:
            sock.close()
            raise x
        sock.close()
        return result

    def _receive(self, sock):
        ''' Wait for a messag from the server and parse it acording to the
            message type.
        '''
        mtype = sock.recv(1)
        if len(mtype) != 1:
            sock.close()
            raise ClientCommunicationException('Could not receive the message '
                    'type from the server.')

        if ord(mtype) == 0x61:
            return self._parse_sjson_data(sock)
        else:
            sock.close()
            raise ClientCommunicationException('Received an unsuported '
                    'communication type. Got: %2x' % ord(mtype))

    def _prepare_sjson_data(self, msg):
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

    def _parse_sjson_data(self, sock):
        ''' Read the sjson object from the given socket. Only the message type
            must be read from the sock object.

            @param sock: The socket to read the rest of the message only the
                    message type should be read from the socket.
            @return: the dictionary/list or other basic type parsed with the
                    json parser.
        '''
        size_data = sock.recv(4)
        if not len(size_data) == 4:
            raise ClientCommunicationException('Could not receive the message'
                    "header. Expected 4 bytes but got: %d" % len(size_data))
        length = ((ord(size_data[0]) << 24) + (ord(size_data[1]) << 16) +
                (ord(size_data[2]) << 8) + ord(size_data[3]))
        if length == 0:
            return None

        data = sock.recv(length)
        if not len(data) == length:
            raise ClientCommunicationException('Could not receive all the data'
                    ' from the client. Expected %d bytes but got: %d' %
                    (length, len(data)))

        return json.loads(data)
