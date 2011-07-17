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
''' Utilities for getting the different application specific directories.
'''

import sys
import os


class AppDirsException(BaseException):
    ''' This exception gets thrown if one of the app dirs functions have 
        problems during execution.
    '''


def user_data_dir(appname, appauthor=None, version=None, roaming=False):
    ''' Get the path to the user specific data directory for this application.

    '''
    pass


def shared_data_dir(appname, appauthor=None, version=None, roaming=False):
    ''' Get the path to the shared data of the application.

    '''
    pass


def config_dir(appname, appauthor=None, version=None, roaming=False):
    ''' Get the global config file for this application
    '''
    pass


def user_config_dir(appname, appauthor=None, version=None, roaming=False):
    ''' Get the user config directory for this application
    '''
    pass


def tmp_data_dir(appname, appauthor=None, version=None, roaming=False):
    ''' Get the path to the directory to store temporary data.
    '''
    pass


def log_dir(appname, appauthor=None, version=None, roaming=False):
    ''' Get the path to the log directory for this application.
    '''
    pass

