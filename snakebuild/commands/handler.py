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
import re
import inspect

from snakebuild.i18n import _, translate
from snakebuild.common import output


CMD_FUNCTION, CMD_DESCRIPTION, CMD_PARAM_LIST = range(3)
SHELL_COMMANDS = {}


class HandleCmdException(BaseException):
    ''' The exception thrown if a problem within the handle command occures.
    '''


def shell_command_register(table):
    ''' Create a decorator to register shell commands to the binary. All added
        commands will be added to the given table.

        @param table: An empty dicionray that is used as the list for the
                shell command handling.
    '''
    def cmd(name):
        ''' The decorator function to register the shell command with the
            given name.

            @param name: The name to call this function
        '''
        def register(func):
            ''' Register the given function/method within the given table.
            '''
            spec = inspect.getargspec(func)
            doc, params = _get_documentation(inspect.getdoc(func))
            arguments_descriptions = []
            if spec.defaults is None:
                arguments = spec.args[2:]
            else:
                arguments = spec.args[2:-len(spec.defaults)]
                for key in spec.args[len(arguments) + 2:]:
                    arguments.append('[{0}]'.format(key))

            for arg in arguments:
                if arg.startswith('['):
                    sarg = arg[1:-1]
                else:
                    sarg = arg
                arguments_descriptions.append((arg, params[sarg]))

            table[name] = func, doc, arguments_descriptions
            return func
        return register
    return cmd


def _get_documentation(doc):
    ''' split the documentation into description and paramters.

        @param doc: The documentation string
    '''
    desc = ""
    params = {}
    lines = doc.split('\n')
    param_search = re.compile(r'@param (?P<name>[a-zA-Z_0-9]*?): '
            '(?P<desc>.*?)$')
    cnt = 0
    for line in lines:
        if line.startswith('@'):
            break
        cnt += 1
        if len(line) == 0:
            desc = '{0}\n'.format(desc.strip())
        else:
            if desc.endswith('\n'):
                desc = '{0}{1}'.format(desc, line.strip())
            else:
                desc = '{0} {1}'.format(desc, line.strip())

    before = ""
    for line in lines[cnt:]:
        result = param_search.search(line)
        if result is None:
            if line.startswith('@') or len(before) == 0:
                before = ""
                continue
            params[before] = '{0} {1}'.format(params[before], line.strip())
        else:
            before = result.group('name')
            if before == 'options' or before == 'config':
                before = ''
                continue
            params[before] = result.group('desc')

    return desc, params


def handle_cmd(cmd_args, options, config):
    ''' Handle the given comman, check if the number of parameters match and
        if it does call the command.

        To register a new command use the function decorator @command like
        this:
        @param('mycall')
        def mycall(options, config, param1, optional=12):
            ' Description of command
              @param options: The options given to this call
              @param config: The configuration object to use
              @param param1: The first paramter given from the shell
              @param optional: The second paramter which is optional and has a
                    default value which is 12.
            '
            TODO

        @param cmd_args: The command including the arguments as a string
        @param options: The options given to this commanand
        @param config: The configuration instance

        @return: True if everything went fine False on error
    '''
    if len(cmd_args) == 0:
        return _print_overview()

    cmd = cmd_args[0].lower()
    if cmd in SHELL_COMMANDS:
        return _call_command(cmd, cmd_args[1:], options, config,
                SHELL_COMMANDS[cmd])
    else:
        output.error(_('Unknown command: {0}').format(cmd))
        return False


def _call_command(cmd, args, options, config, cmd_info):
    ''' Call the given command from the command list. This does some basic
        checking if the paramter count matches the expected count for the given
        command.

        @param cmd: The command that gets called
        @param args: The arguments for the given command given by the user
        @param options: The options set by the user
        @param config: The configuration instance
        @param cmd_info: The command information from the cmd_list

        @return True on success and False on Failure
        @throws HandleCmdException: If the command could not be processed
    '''
    min_cnt = len(cmd_info[CMD_PARAM_LIST])
    max_cnt = min_cnt
    for cmd_name, cmd_desc in cmd_info[CMD_PARAM_LIST]:
        if cmd_name.startswith('['):
            min_cnt -= 1
    if not (min_cnt <= len(args) <= max_cnt):
        if min_cnt == max_cnt:
            output.error(_('The number of parameters did not match the '
                    'expected number of paramters. Got: {0:d}, Expected: '
                    '{1:d}').format(len(args), max_cnt))
        else:
            output.error(_('The number of parameters did not match the '
                    'expected number of paramters. Got: {0:d}, Expected '
                    'between: {1:d} and {2:d}').format(len(args), min_cnt,
                    max_cnt))
        _print_cmd_help_detail(cmd, cmd_info)
        return False

    return cmd_info[CMD_FUNCTION](options, config, *args)


command = shell_command_register(SHELL_COMMANDS)


@command('help')
def _help(options, config, action=None):
    ''' The help command to print the help for a given command or to print a
        list with all available commands.

        @param options: The options given to the call
        @param config: The configuration instance
        @param action: The command to get the help for. If no command is given
                then an overview of all commands will be printed.
    '''
    if action is None:
        return _print_overview()
    else:
        return _print_cmd_help(action, config)


def _print_overview():
    ''' Print an overview over all the commands available. '''
    output.message(_("This is the overview over all the supported commands "
            "for the {0}.").format(os.path.basename(sys.argv[0])))
    print ""
    print _("Commands:")
    for cmd, info in SHELL_COMMANDS.iteritems():
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
    output.message("{0}{1}{2}".format(cmd, " " * space,
            output.shorten_message(translate(info[CMD_DESCRIPTION].strip()))),
            indent=' ' * 8, first_indent=" " * 2)


def _print_cmd_help(cmd, config):
    ''' Print help for the given command

        @param cmd: The command to get the help for
        @param config: The configuration instance
    '''
    if cmd in SHELL_COMMANDS:
        _print_cmd_help_detail(cmd, SHELL_COMMANDS[cmd])
    elif cmd == 'configfile':
        print "CONFIG FILE HELP"
    else:
        output.error(_("The given command is unknown: {0}\n").format(cmd))
        return False

    return True


def _print_cmd_help_detail(cmd, cmd_info):
    ''' Print the help for one given command
        @param cmd: The command to print the help for
        @param cmd_info: The command information from the COMMAND_LIST
    '''
    print ""
    output.message(translate(cmd_info[CMD_DESCRIPTION].strip()))
    print ""
    print "  {0} {1} {2}".format(os.path.basename(sys.argv[0]), cmd,
            " ".join([el[0] for el in cmd_info[CMD_PARAM_LIST]]))
    print ""
    print _("Parameters:")
    for key, desc in cmd_info[CMD_PARAM_LIST]:
        i = len(key)
        if i <= 8:
            space = (12 - i)
        else:
            space = 4 - (i % 4)
        output.message("{0}{1}{2}".format(key, " " * space,
                translate(desc.strip())), indent=" " * 8, first_indent=" " * 2)
        print ""
