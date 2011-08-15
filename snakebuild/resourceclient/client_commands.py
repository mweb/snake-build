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
''' This files contains the dictionary with all the commands which are
    supported by the resource client command.
'''

from snakebuild.common import output

COMMANDS = {
        'help': (_help,
                'Use the help command with the name of the command you '
                'wish to get help for.',
                ['[COMMAND]'],
                {'[COMMAND]': 'The command to get the help for.'}),
        'acquire': (None, '', [], {})}


CMD_FUNCTION, CMD_DESCRIPTION, CMD_PARAMETERS_LIST, CMD_PARAMETERS_DICT = \
        range(3)


class CMDException(BaseException):
    ''' The exception thrown if a problem with the command handling occures.
    '''


def _help(args, options):
    ''' The help command to print the help for a given command or to print a
        list with all available commands.

        @args: The arguments list the first element is always the command it
            self (help).
        @options: The dictionary with all the options set
    '''
    if not (len(args) >= 0 or args[0].lower() == 'help'):
        output.error("_help function called for the wrong command.")
        raise CMDException("Wrong command used %s" % args)

    if len(args) == 1:
        _print_overview()
    else:
        _print_cmd_help(args[1])


def _print_overview():
    ''' Print an overview over all the commands available. '''
    print "HEP"


def _print_cmd_help(cmd):
    ''' Print help for the given command

        @param cmd: The command to get the help for
    '''
    if cmd in COMMANDS:
        values = COMMANDS[cmd]
        print ""
        output.message(values[CMD_DESCRIPTION])
        print ""
        print "  %s %s" % (cmd, " ".join(values[CMD_PARAMETERS_LIST]))
        print ""
        for key in values[CMD_PARAMETERS_LIST]:
            value = values[CMD_PARAMETERS_DICT][key]
            output.message("%s\t%s" % (key, value), indent="\t\t", 
                    first_indent="  ")
            print ""
    elif cmd == 'configfile':
        print "CONFIG FILE HELP"
    else:
        output.error("The given command is unknwon: %s\n" % cmd)
        _print_overview()

    return

