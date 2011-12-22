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
''' A simple function to get the current running platform. This is necessary
    for several parts of the application.
'''

import sys

from snakebuild.i18n import _

__installed__ = False

WINDOWS, MACOS, LINUX, UNKNOWN = range(4)


def get_platform():
    ''' Get the platform type for the current running system. '''
    if sys.platform.startswith('win'):
        return WINDOWS
    elif sys.platform == 'darwin':
        return MACOS
    elif sys.platform.startswith('linux'):
        return LINUX
    else:
        print _("OS type could not be found. We try the Linux configuration "
                "if this doesn't work switch to a supported platform.")
        return LINUX


def is_installed():
    ''' Check if the application is installed or if it is running directly from
        the source code.
        @return True if it is installed and False if it is running from the
                source
    '''
    return __installed__
