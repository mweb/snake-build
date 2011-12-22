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

from snakebuild.i18n import _
from snakebuild.communication.messages import prepare_sjson_data
from snakebuild.communication.commandstructure import FUNCTION, PARAMETERS, \
        SIGNED, prepare_error

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
        elif ord(data[0]) == 0x62:
            self._parse_signed_request()
        else:
            LOG.error(_('The message type received is not supported. got: '
                    '0x{0:02x}').format(ord(data[0])))
            return

    def _parse_signed_request(self):
        ''' Check if the given request is correctly signed. If yes forward it
            to the _sjson_request_handler.
            The message it self is not encrypted.
        '''
        # TODO implement the signature check
        pass
        #self._sjson_request_handler(cmd, True)

    def _parse_sjson_request(self):
        ''' Get a sjson request and call the appropriate command if available.
        '''
        length_data = self.request.recv(4)
        if not len(length_data) == 4:
            LOG.error(_('The message received did not return 4 bytes for the '
                    'length of th message: Only got: {0:d}').format(
                    len(length_data)))
            return
        length = ((ord(length_data[0]) << 24) + (ord(length_data[1]) << 16) +
                (ord(length_data[2]) << 8) + ord(length_data[3]))

        data = self.request.recv(length)
        if not len(data) == length:
            LOG.error(_('Wrong length of data received: Expected {0:d} but '
                    'got {0:d}').format(length, len(data)))
            return
        try:
            cmd = json.loads(data)
        except ValueError:
            LOG.error(_('Could not parse the received data. Not a valid json '
                    'string.'))
            return
        self._sjson_request_handler(cmd, False)

    def _sjson_request_handler(self, cmd, signed):
        ''' Check the cmd dictionary which was parsed from a sjson if it is a
            valid command. If it is call it.

            @param cmd: The loaded dictionary
            @param signed: If set to true then the command was called with a
                valid signature. Which means it should be allowd to to
                administrativ tasks.
        '''
        if not 'cmd' in cmd:
            LOG.error(_("The message received did not have a 'cmd' key."))
            return
        if not 'parameters' in cmd:
            LOG.error(_("The message received did not have a 'parameters' "
                "key."))
            return

        answer = _handle_cmd(cmd['cmd'], cmd['parameters'],
                self.server.commands, self.server.data, signed)

        answerdump = prepare_sjson_data({'cmd': cmd['cmd'],
                'parameters': (answer)})

        self.request.send(answerdump)


def _handle_cmd(cmd, parameters, commands, data, signed):
    ''' Handle the given command if it is specified within the commands.

        @param cmd: The command as a string
        @param parameters: The parameters for the command
        @param commands: The dictionary with the suported commands
        @param data: The data object to provide to the commands
        @param signed: The switch if the message was sent signed or not.
                Certain command are not allowed to be called without signature.

        @return the answer of the command or an error message if the parameters
            are not valid.
    '''
    cmd = cmd.lower()
    if cmd in commands:
        return _call_cmd(commands[cmd], cmd, parameters, data, signed)
    else:
        cmd_list = dict((k.lower(), v) for k, v in commands.iteritems())
        if cmd.lower() in cmd_list:
            cmd = cmd.lower()
            return _call_cmd(cmd_list[cmd], cmd, parameters, data, signed)
        else:
            return prepare_error(_('The requested command is not supported '
                    'by this server instance. Command: {0}').format(cmd))


def _call_cmd(cmd, cmd_name, parameters, data, signed):
    ''' Call the given command and performe some sanity checks if the
        requested command is valid.

        @param cmd: The command dictionary entry
        @param cmd_name: The name of the command.
        @param parameters The parameters for the command
        @param data: The data object to pass to the command
        @param signed: The switch whicht is enabled if the message was sent
            with a valid signature.

        @return the answer of the command or an error message if the parameters
            are not valid.
    '''
    for param in cmd[PARAMETERS]:
        if param.startswith('['):
            # we don't look for the optional parameters right now
            continue
        if not param in parameters:
            return prepare_error(_('The parameter ({0}) is required for the '
                    'call of this command, but is not '
                    'available.').format(param))
    if parameters is not None:
        for key in parameters.iterkeys():
            if key in cmd[PARAMETERS]:
                continue
            elif ("[%s]" % key) in cmd[PARAMETERS]:
                continue
            else:
                return prepare_error(_('The parameter ({0}) is not specified '
                        'for the call of this command.').format(key))
    if cmd[SIGNED] and not signed:
        return prepare_error(_('You are not allowed to call this command. '
                'This command is only allowed for verified users.'))
    if parameters is None:
        return cmd[FUNCTION](data)
    else:
        return cmd[FUNCTION](data, **parameters)
