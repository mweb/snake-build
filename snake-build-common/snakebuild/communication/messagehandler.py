# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import SocketServer
import json
import logging

log = logging.getLogger('snakebuild.communication.messagehandler')


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
            log.error('The message type received is not supported. got: %x' %
                    ord(data[0]))
            return

    def _parse_sjson_request(self):
        ''' Get a sjson request and call the appropriate command if available.
        '''
        length_data = self.request.recv(4)
        if not len(length_data) == 4:
            log.error('The message received did not return 4 bytes for the '
                    'length of th message: Only got: %d' % len(length_data))
            return
        length = ((ord(length_data[0]) << 24) + (ord(length_data[1]) << 16) +
                (ord(length_data[2]) << 8) + ord(length_data[3]))

        data = self.request.recv(length)
        if not len(data) == length:
            print "HERE %d / %d" % (len(data), length)
            log.error('Wrong length of data received: Expected %d but got %d' %
                    (length, len(data)))
            return
        try:
            cmd = json.loads(data)
        except ValueError:
            log.error('Could not parse the received data. Not a valid json '
                    'string.')
            return
        if not 'cmd' in cmd:
            log.error("The message received did not have a 'cmd' key.")
            return
        if not 'parameters' in cmd:
            log.error("The message received did not have a 'parameters' key.")
            return

        self._handle_cmd(cmd['cmd'], cmd['parameters'],
                self.request.server.commands)

    def _handle_cmd(self, cmd, parameters, commands):
        ''' Handle the given command if it is specified within the commands.

            @param cmd: The command as a string
            @param parameters: The paramters for the command
            @param commands: The dictionary with the suported commands
        '''
        cmd = cmd.lower()
        if cmd in commands:
            return commands[cmd][0](cmd, parameters)
        else:
            cmd_list = dict((k.lower(), v) for k, v in commands.iteritems())
            if cmd.lower() in cmd_list:
                return cmd_list[cmd][0](cmd, parameters)
            else:
                log.error("The requested command '%d' is not supported by the "
                        "given server implementation." % cmd)
                return
