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
''' The command line parser of the sb-resourceserver application. '''

from argparse import ArgumentParser

from snakebuild.i18n import _
from snakebuild.commands import register_argument_parsers, \
        shell_command_register

SHELL_COMMANDS = {}
command = shell_command_register(SHELL_COMMANDS)


def parse_command_line(args, version):
    ''' Read the command line and parse it. All command line arguments are
        specified within this method.

        @param args: The arguments string/list to parse
        @param version: The version string to show.
        @return: the parsed arguments
    '''
    parser = ArgumentParser(description=_('The resourceserver to ask for '
            'build or test resources.'), version=version)
    parser.add_argument('--configfile', '-f',
        help=_('The configfile to load. This will be the last file to be '
        'loaded and it will be overwritten for storing a new '
        'configuration.'), default=None)

    register_argument_parsers(parser, SHELL_COMMANDS)

    return parser.parse_args(args)
