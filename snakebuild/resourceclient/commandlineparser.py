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
''' The command line parser of the sb-resourceclient application. '''

from argparse import ArgumentParser

from snakebuild.i18n import _


def parse_command_line(register_func, version):
    ''' Read the command line and parse it. All command line arguments are
        specified within this method.

        @param regiser_func: the function to call to register all the
                subparsers
        @param version: The version string to show.
        @return: the parsed arguments
    '''
    parser = ArgumentParser(description=_('The resource client to acquire '
            'resources form the resource server.'), version=version)
    parser.add_argument('--configfile', '-f', default=None,
        help=_('The configfile to load. This will be the last file to be '
        'loaded and it will be overwritten for storing a new '
        'configuration.'))
    parser.add_argument('--username', help=_('Specify the name of the user to'
        ' use for talking with the resource server. If nothing is specified '
        'the value from the config file is taken.'), default=None)
    parser.add_argument('--server', help=_('Specify the location of the '
        'server to connect to. The port is taken from the config file if not '
        'specified seperatly.'), default=None)
    parser.add_argument('--port', help=_('Specify the network port the server'
        ' is listening. If nothing is specified the port from the config file '
        'is taken.'), default=None)

    register_func(parser)

    return parser.parse_args()
