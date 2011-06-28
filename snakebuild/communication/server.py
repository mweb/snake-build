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
''' The Server object proovides a server instance which runs forever or until
    the shutdown method is called. It will listen for clients and forward
    all connections to the MessageHandler. The Server requires a dictionary
    with all supported commands with a function to call.
'''

import threading
import socket
import time
import logging
import SocketServer

from snakebuild.communication.messagehandler import MessageHandler

LOG = logging.getLogger('snakebuild.communication.messagehandler')


class ServerCommunicationException(BaseException):
    ''' The exception that gets trown on an error during the communication with
        the client.
    '''


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    ''' Get a multithreaded socket server. '''


class Server(object):
    ''' This class is simple wrapper class for a server class which handles
        sjson messages. The parsing of the messages is done. The user of this
        class must provide a list with commands and the commands to call on
        this commands.

        For a description of the protocol see the Snake-Build-Dev
        documentation.
    '''
    # this defines the known message types
    SJSON, UNKNWON = range(2)

    def __init__(self, host, port, commands):
        ''' Create a server object with the given host and port. The server
            does not start listening until the run method is called.

            The commands dictionary has the commands that are supported as keys
            and as the value a tuple with the first element a callable which
            takes two parameters. 1. command 2. parameters

            @param host: The host address (as a string)
            @param port: The network port to use for the connection (as int)
            @param commands: A dictionary with all the supported commands and
                    the methods to call if such a command get received.
        '''
        self.host = host
        self.port = port
        self.commands = commands
        self.server = None
        self.server_running = True

    def run(self):
        ''' Start the server. This method will not return until the server
            gets stoped.
        '''
        srvr = threading.Thread(target=self.run_server)
        srvr.start()

        while self.server_running:
            try:
                time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                break

        self.server_running = False
        if self.server is not None:
            self.server.shutdown()

    def run_server(self):
        ''' This method starts listening on the network host:port for clients.
            This method does not return until the server gets stopped.
        '''
        self.server = None
        while self.server is None and self.server_running:
            try:
                self.server = ThreadedTCPServer((self.host, self.port),
                        MessageHandler)
            except socket.error:
                LOG.warning('Could not open network connection, will try again'
                        ' within a few seconds.')
                time.sleep(2)
        LOG.info('Server started.')

        self.server.commands = self.commands
        if self.server_running:
            self.server.serve_forever()

        LOG.info('Shutdown the server.')
