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
''' This package provides the generic methods to handle the commands for the
    command line tools.
'''

import sys
import os

from snakebuild.common import output


GENERIC_COMMANDS = {'help': (None, 'This is the help command. This command '
                'provides informatin about all the supported commands and the '
                'configuration. If not command is given an overview over all '
                'the commands will be shown.',
                ['[COMMAND]'], {'[COMMAND]': 'The command to get the help '
                    'for. In addition to the commands it is possible '
                    'to request help for the configuratin file with: '
                    'configfile'}),
                'configfile': (None, 'This shows the information about the '
                    'config file. This will give an overview over all the '
                    'available configuration options.', [], {})}


CMD_FUNCTION, CMD_DESCRIPTION, CMD_PARAM_LIST, CMD_PARAM_DICT = range(4)


class HandleCmdException(BaseException):
    ''' The exception thrown if a problem within the handle command occures.
    '''


def handle_cmd(cmd_args, options, cmd_list):
    ''' Handle the given comman, check if the number of passwords match and if
        it does call the command.

        The command list must be a dictionary, which has a tuple with the
        following elements with this order:
        - the function to call
        - description as text (string)
        - a list with all the paramters as a list
        - a dictionary with all the parameters as the key and a description for
            each parameter.

        Example: { 'help': (_help, 'description of help',
                            ['COMMAND', '[OPTIONAL]'],
                            {'COMMAND' : 'description',
                                '[OPTIONAL]': 'description two'}
                }

        If a parameter has rectangular brackets then it is optinal and no error
        will be thrown if not given.

        @param cmd_args: The command including the arguments as a string
        @param options: The options given to this commanand
        @param cmd_list: The complete command list to search for the command

        @return: True if everything went fine False on error
    '''
    if len(cmd_args) == 0:
        _print_overview(cmd_list)

    cmd = cmd_args[0].lower()
    if cmd in cmd_list:
        pass
    elif cmd == 'help':
        _help(cmd, cmd_args[1:], options, cmd_list)
    else:
        raise HandleCmdException('Unknown Command %s' % cmd)


def _help(cmd, parameters, options, cmd_list):
    ''' The help command to print the help for a given command or to print a
        list with all available commands.

        @cmd: The command string that lead to this call
        @options: The dictionary with all the options set
        @cmd_list: The dictionar with all the commands and its descriptions
        @parameter: The paramter given to the help command (default None) If
            None then an overview over all the commands will be printed.
    '''
    if not (cmd.lower() == 'help'):
        output.error("_help function called for the wrong command.")
        raise HandleCmdException("Wrong command used %s" % cmd)

    if len(parameters) == 0:
        _print_overview(cmd_list)
    else:
        _print_cmd_help(parameters[0], cmd_list)


def _print_overview(cmd_list):
    ''' Print an overview over all the commands available. '''
    output.message("This is the overview over all the supported commands for "
            "the %s." % os.path.basename(sys.argv[0]))
    print ""
    print "Commands:"
    for cmd, info in GENERIC_COMMANDS.iteritems():
        _print_short_help(cmd, info)
    for cmd, info in cmd_list.iteritems():
        _print_short_help(cmd, info)


def _print_short_help(cmd, info):
    ''' Print the short help for a command
        @param cmd: The command to print the help for
        @param info: The information for the help command
    '''
    i = len(cmd)
    if i <= 8:
        space = (12 - i)
    else:
        space = 4 - (i % 4)
    output.message("%s%s%s" % (cmd, " " * space, info[CMD_DESCRIPTION]),
            indent='        ', first_indent="  ")


def _print_cmd_help(cmd, cmd_list):
    ''' Print help for the given command

        @param cmd: The command to get the help for
    '''
    if cmd == 'help':
        cmd_list = GENERIC_COMMANDS
    if cmd in cmd_list:
        values = cmd_list[cmd]
        print ""
        output.message(values[CMD_DESCRIPTION])
        print ""
        print "  %s %s" % (cmd, " ".join(values[CMD_PARAM_LIST]))
        print ""
        for key in values[CMD_PARAM_LIST]:
            value = values[CMD_PARAM_DICT][key]
            output.message("%s\t%s" % (key, value), indent="\t\t",
                    first_indent="  ")
            print ""
    elif cmd == 'configfile':
        print "CONFIG FILE HELP"
    else:
        output.error("The given command is unknwon: %s\n" % cmd)
        return _print_overview(cmd_list)

    return True
