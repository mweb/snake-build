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

import inspect

from snakebuild.i18n import _
from snakebuild.common import output


CMD_FUNCTION, CMD_DESCRIPTION, CMD_PARAM_LIST = range(3)
#SHELL_COMMANDS = {}


class HandleCmdException(BaseException):
    ''' The exception thrown if a problem within the handle command occures.
    '''


def shell_command_register(table):
    ''' Create a decorator to register shell commands to the binary. All added
        commands will be added to the given table.

        @param table: An empty dicionray that is used as the list for the
                shell command handling.
    '''
    def cmd(name, arguments):
        ''' The decorator function to register the shell command with the
            given name.

            @param name: The name to call this function
            @param arguments: The list with all the arguments for this
                    subcommand
        '''
        def register(func):
            ''' Register the given function/method within the given table.
            '''
            spec = inspect.getargspec(func)
            # TODO validate function parameters (args, config)
            doc = _get_documentation(inspect.getdoc(func))
            table[name] = func, doc, arguments
            return func
        return register
    return cmd


def _get_documentation(doc):
    ''' split the documentation into description and paramters.

        @param doc: The documentation string
    '''
    desc = ""
    lines = doc.split('\n')
    cnt = 0
    for line in lines:
        if line.startswith('@') or line.startswith(':'):
            break
        cnt += 1
        if len(line) == 0:
            desc = '{0}\n'.format(desc.strip())
        else:
            if desc.endswith('\n'):
                desc = '{0}{1}'.format(desc, line.strip())
            else:
                desc = '{0} {1}'.format(desc, line.strip())

    return desc


def register_argument_parsers(parser, table):
    ''' Register all the commands within the given argument parser.

        @param parser: The argument parser to add all the subcommands
        @param table: The shell comannd table
    '''
    subparsers = parser.add_subparsers(help=_('Commands'), dest='command')

    for cmd, values in table.iteritems():
        cparser = subparsers.add_parser(cmd, help=values[CMD_DESCRIPTION])
        for names, parameters in values[CMD_PARAM_LIST]:
            cparser.add_argument(*names, **parameters)


def handle_cmd(table, args, config):
    ''' Handle the given command.

        To register a new command use the function decorator @command like
        this:
        @command('mycall', _('DESCRIPTION'), (
                (('--back',), (action='store_true', help=_('background')))
            ))
        def mycall(args, config):
            ' Description of command
              @param args: The parsed argument values.
              @param config: The configuration object to use
            '
            TODO

        The command decorator must be defined before in a local environment.

        command = shell_command_register(SHELL_COMMANDS)

        @param args: The command including all the arguments
        @param config: The configuration instance

        @return: True if everything went fine False on error
    '''
    cmd = args.command
    if cmd in table:
        return table[cmd][CMD_FUNCTION](args, config)
    else:
        output.error(_('Unknown command: {0}').format(cmd))
        return False


#command = shell_command_register(SHELL_COMMANDS)
