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
''' The MessageHandler gets created from the server and does the handling of
    messages received from the client. The supported commands are specified
    within the server instance (commands)
'''

import SocketServer
import json
import logging

from snakebuild.communication.messages import prepare_sjson_data

LOG = logging.getLogger('snakebuild.communication.messagehandler')


class MessageHandler(SocketServer.BaseRequestHandler):
    ''' Receive the messags from the client and handle the received command
        if the command is defined within the server.commands dictionary.
        If not log the message and ignore it. (Send error message)
    '''
    def handle(self):
        ''' Handle the data sent and check what to with it. '''
        data = self.request.recv(1)
        if not len(data) == 1:
            return
        if ord(data[0]) == 0x61:
            self._parse_sjson_request()
        else:
            LOG.error('The message type received is not supported. got: %x' %
                    ord(data[0]))
            return

    def _parse_sjson_request(self):
        ''' Get a sjson request and call the appropriate command if available.
        '''
        length_data = self.request.recv(4)
        if not len(length_data) == 4:
            LOG.error('The message received did not return 4 bytes for the '
                    'length of th message: Only got: %d' % len(length_data))
            return
        length = ((ord(length_data[0]) << 24) + (ord(length_data[1]) << 16) +
                (ord(length_data[2]) << 8) + ord(length_data[3]))

        data = self.request.recv(length)
        if not len(data) == length:
            LOG.error('Wrong length of data received: Expected %d but got %d' %
                    (length, len(data)))
            return
        try:
            cmd = json.loads(data)
        except ValueError:
            LOG.error('Could not parse the received data. Not a valid json '
                    'string.')
            return
        if not 'cmd' in cmd:
            LOG.error("The message received did not have a 'cmd' key.")
            return
        if not 'parameters' in cmd:
            LOG.error("The message received did not have a 'parameters' key.")
            return

        answer = _handle_cmd(cmd['cmd'], cmd['parameters'],
                self.server.commands, self.server.data)

        answerdump = prepare_sjson_data({'cmd': cmd['cmd'],
                'parameters': (answer)})

        self.request.send(answerdump)


def _handle_cmd(cmd, parameters, commands, data):
    ''' Handle the given command if it is specified within the commands.

        @param cmd: The command as a string
        @param parameters: The paramters for the command
        @param commands: The dictionary with the suported commands
        @param data: The data object to provide to the commands
    '''
    cmd = cmd.lower()
    if cmd in commands:
        return commands[cmd][0](cmd, parameters, data)
    else:
        cmd_list = dict((k.lower(), v) for k, v in commands.iteritems())
        if cmd.lower() in cmd_list:
            return cmd_list[cmd][0](cmd, parameters, data)
        else:
            LOG.error("The requested command '%s' is not supported by the "
                    "given server implementation." % cmd)
            return
