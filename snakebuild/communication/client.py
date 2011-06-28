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
''' The Client object offers a method to communicate with a server with the
    sjson protocol. It does pack the messages and unpack the received messages.
'''

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

        See the Snake-Build Dev documentation for more information about the
        protocol.
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

    def send(self, mtype, cmd, param, no_answer=False):
        ''' Send a message to the server ans try to receive an answer if this
            isn't disabled.

            The param can be anything from a dictionary, list to an int, float
            or any other basic type. Even None. It is possible to have
            multiple nexted dicts and list but it should be kept as simple
            as possible.

            The answer of this command returns the command and the paramers
            as a python type. This might be dictionary or a list or any other
            python basic type and as with the send param it can be nested.

            @param mtype: The type of the message to send. Use the defined
                types of this class (SJSON)
            @param cmd: The command to send to the server.
            @param param: The message parameters to send. Must be a python
                    basic type (dictionary, list, int, float, boolean, string,
                    None)
            @param no_answer: If set to true no answer expected so don't wait
                    for it.

            @return: The answer from the server as a tuple (cmd, parameters)
        '''
        if mtype >= self.UNKNWON:
            raise ClientCommunicationException('The given message type is not '
                    'supported.')

        if mtype == self.SJSON:
            data = _prepare_sjson_data({'cmd': cmd, 'parameters': param})
#        elif mytype == OTHER:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((self.host, self.port))
        sock.send(data)

        if no_answer:
            sock.close()
            return (None, None)
        try:
            result = _receive(sock)
        except KeyboardInterrupt, intr:
            sock.close()
            raise intr
        sock.close()
        return result


def _receive(sock):
    ''' Wait for a messag from the server and parse it acording to the
        message type.

        @param sock: The socket to use for receiving the data
        @return: the command param tuple (cmd, parameters)
    '''
    mtype = sock.recv(1)
    if len(mtype) != 1:
        sock.close()
        raise ClientCommunicationException('Could not receive the message '
                'type from the server.')

    if ord(mtype) == 0x61:
        return _parse_sjson_data(sock)
    else:
        sock.close()
        raise ClientCommunicationException('Received an unsuported '
                'communication type. Got: %2x' % ord(mtype))


def _prepare_sjson_data(msg):
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


def _parse_sjson_data(sock):
    ''' Read the sjson object from the given socket. Only the message type
        must be read from the sock object.

        The answer of this command returns the command from the json
        string and the paramers as a python type might be dictionary or
        a list or any other python basic type.

        @param sock: The socket to read the rest of the message only the
                message type should be read from the socket.
        @return: a tuple (command, parameters)
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

    answer = json.loads(data)
    if not 'cmd' in answer:
        raise ClientCommunicationException('The answer received did not '
                "have a 'cmd' key.")
    if not 'parameters' in answer:
        raise ClientCommunicationException('The answer received did not '
                "have a 'parameters' key.")

    return answer['cmd'], answer['parameters']
