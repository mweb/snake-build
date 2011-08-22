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
        return _print_overview(cmd_list)

    cmd = cmd_args[0].lower()
    if cmd in cmd_list:
        return _call_command(cmd, cmd_args[1:], options, cmd_list[cmd])
    elif cmd == 'help':
        return _help(cmd, cmd_args[1:], cmd_list)
    else:
        raise HandleCmdException('Unknown Command %s' % cmd)


def _help(cmd, parameters, cmd_list):
    ''' The help command to print the help for a given command or to print a
        list with all available commands.

        @cmd: The command string that lead to this call
        @parameter: The paramter given to the help command (default None) If
            None then an overview over all the commands will be printed.
        @cmd_list: The dictionar with all the commands and its descriptions
    '''
    if not (cmd.lower() == 'help'):
        output.error("_help function called for the wrong command.")
        raise HandleCmdException("Wrong command used %s" % cmd)

    if len(parameters) == 0:
        return _print_overview(cmd_list)
    else:
        return _print_cmd_help(cmd, cmd_list)


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

    return True


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
        _print_cmd_help_detail('help', GENERIC_COMMANDS['help'])
    elif cmd in cmd_list:
        _print_cmd_help_detail(cmd, cmd_list[cmd])
    elif cmd == 'configfile':
        print "CONFIG FILE HELP"
    else:
        output.error("The given command is unknwon: %s\n" % cmd)
        _print_overview(cmd_list)
        return False

    return True


def _print_cmd_help_detail(cmd, cmd_info):
    ''' Print the help for one given command
        @param cmd: The command to print the help for
        @param cmd_info: The command information from the COMMAND_LIST
    '''
    print ""
    output.message(cmd_info[CMD_DESCRIPTION])
    print ""
    print "  %s %s %s" % (os.path.basename(sys.argv[0]), cmd,
            " ".join(cmd_info[CMD_PARAM_LIST]))
    print ""
    print "Parameters:"
    for key in cmd_info[CMD_PARAM_LIST]:
        value = cmd_info[CMD_PARAM_DICT][key]
        i = len(key)
        if i <= 8:
            space = (12 - i)
        else:
            space = 4 - (i % 4)
        output.message("%s%s%s" % (key, " " * space, value), indent="        ",
                first_indent="  ")
        print ""


def _call_command(cmd, args, options, cmd_info):
    ''' Call the given command from the command list. This does some basic
        checking if enough but not too man variables are provided for the given
        command.

        @param cmd: The command that gets called
        @param args: The arguments for the given command given by the user
        @param options: The options set by the user
        @param cmd_info: The command information from the cmd_list

        @return True on success and False on Failure
        @throws HandleCmdException: If the command could not be processed
    '''
    min_cnt = len(cmd_info[CMD_PARAM_LIST])
    max_cnt = min_cnt
    for cmd_name in cmd_info[CMD_PARAM_LIST]:
        if cmd_name.startswith('['):
            min_cnt -= 1
    if not (min_cnt <= len(args) <= max_cnt):
        if min_cnt == max_cnt:
            output.error('The number of parameters did not match the expected '
                    'number of paramters. Got: %d, Expected: %d' %
                    (len(args), max_cnt))
        else:
            output.error('The number of parameters did not match the expected '
                    'number of paramters. Got: %d, Expected between: %d and '
                    '%d ' % (len(args), min_cnt, max_cnt))
        _print_cmd_help_detail(cmd, cmd_info)
        return False

    return cmd_info[CMD_FUNCTION](cmd, options, *args)
