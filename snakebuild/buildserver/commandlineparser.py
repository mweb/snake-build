# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2012 Mathias Weber <mathew.weber@gmail.com>
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
''' The command line parser of the sb-buildserver application. '''

from optparse import OptionParser

from snakebuild.i18n import _

def parse_command_line():
    ''' Read the command line and parse it. All command line arguments are
        specified within this method.
    '''
    usage = _('usage: %prog [OPTIONS]\n')

    parser = OptionParser(usage)
    parser.add_option('-f', '--configfile', dest='configfile', metavar='FILE',
        help=_('The configfile to load. This will be the last file to be '
        'loaded and it will be overwritten for storing a new '
        'configuration.'), default=None)
    parser.add_option('--background', dest='background', action='store_true',
            help=_('Run the build server in background'), default=False)
    parser.add_option('-v', '--version', dest='version', action='store_true',
            help=_('Ask for the version.'), default=False)

    (options, args) = parser.parse_args()

    return options, args
