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

    This code is inspired by http://github.com/ActiveState/appdirs and a few
    functions are copied directly from it. The original code has the following
    License.

    # This is the MIT license

    Copyright (c) 2010 ActiveState Software Inc.

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
'''

import sys
import os

from snakebuild.snakebuildconfig import DATA_DIRECTORY, CONFIG_DIRECTORY


class AppDirsException(BaseException):
    ''' This exception gets thrown if one of the app dirs functions have
        problems during execution.
    '''


def get_user_config_path(appname, appauthor=None, version=None, roaming=False):
    ''' Get the path to the user specific config path for this application.

        @appname: The name of the application (this is used for the directory
                within the data directory.
        @appauthor: The name of the author (this is used on windows for getting
                the right directory within the data dir.
        @version: The version of app. This is only used if required. For
                example if the application should allow multiple installation
                on one system.
        @roaming: Boolean value set to true if the roaming profile should be
                used on windows.

        @return: the path to the data/config directory for the given
                application
    '''
    if sys.platform.startswith('win'):
        if appauthor is None:
            raise AppDirsException("On windows the 'appauthor' must be "
                    "specified")
        const = roaming and "CSIDL_APPDATA" or "CSIDL_LOCAL_APPDATA"
        path = os.path.join(_get_win_folder(const), appauthor, appname)
    elif sys.platform == 'darwin':
        path = os.path.join(
                os.path.expanduser('~/Library/Application Support/'), appname)
    else:
        path = os.path.join(os.path.expanduser('~/.config'), appname.lower())

    if version:
        path = os.path.join(path, version)

    return path


def get_config_path(appname, appauthor=None, version=None, roaming=False):
    ''' Get the path to the global config path for this application.

        @appname: The name of the application (this is used for the directory
                within the data directory.
        @appauthor: The name of the author (this is used on windows for getting
                the right directory within the data dir.
        @version: The version of app. This is only used if required. For
                example if the application should allow multiple installation
                on one system.
        @roaming: Boolean value set to true if the roaming profile should be
                used on windows.

        @return: the path to the data/config directory for the given
                application
    '''
    if CONFIG_DIRECTORY is not None:
        return os.path.join(os.path.dirname(__file__), '..' ,CONFIG_DIRECTORY)

    if sys.platform.startswith('win'):
        path = get_user_config_path(appname, appauthor, version, roaming)
    elif sys.platform == 'darwin':
        path = get_user_config_path(appname, appauthor, version, roaming)
    else:
        path = os.path.join('etc', appname.lower())

    if version:
        path = os.path.join(path, version)

    return path


def get_data_path(appname, appauthor=None, version=None):
    ''' Get the path to the shared data of the application. This data are
        readonly and should not be changed and they are installed by the
        application.

        @appname: The name of the application (this is used for the directory
                within the data directory.
        @appauthor: The name of the author (this is used on windows for getting
                the right directory within the data dir.
        @version: The version of app. This is only used if required. For
                example if the application should allow multiple installation
                on one system.

        @return: the path to the shared data directory for the given
                application
    '''
    pass


def tmp_data_path():
    ''' Get the path to the directory to store temporary data.

        @return: the path to the tmp data directory
    '''
    pass


def log_path(appname, appauthor=None, version=None):
    ''' Get the path to the log directory for this application.

        @appname: The name of the application (this is used for the directory
                within the data directory.
        @appauthor: The name of the author (this is used on windows for getting
                the right directory within the data dir.
        @version: The version of app. This is only used if required. For
                example if the application should allow multiple installation
                on one system.

        @return: the path to the log directory for the given application
    '''
    pass


def _get_win_folder_from_registry(csidl_name):
    ''' This is a fallback technique at best. I'm not sure if using the
        registry for this guarantees us the correct answer for all CSIDL_*
        names.
    '''
    import _winreg

    shell_folder_name = {
        "CSIDL_APPDATA": "AppData",
        "CSIDL_COMMON_APPDATA": "Common AppData",
        "CSIDL_LOCAL_APPDATA": "Local AppData",
    }[csidl_name]

    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    directory, dtype = _winreg.QueryValueEx(key, shell_folder_name)
    return directory


def _get_win_folder_with_pywin32(csidl_name):
    ''' Get the folder on windows with the help of pywin32 '''
    from win32com.shell import shellcon, shell
    directory = shell.SHGetFolderPath(0, getattr(shellcon, csidl_name), 0, 0)
    # Try to make this a unicode path because SHGetFolderPath does
    # not return unicode strings when there is unicode data in the
    # path.
    try:
        directory = unicode(directory)

        # Downgrade to short path name if have highbit chars. See
        # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
        has_high_char = False
        for char in directory:
            if ord(char) > 255:
                has_high_char = True
                break
        if has_high_char:
            try:
                import win32api
                directory = win32api.GetShortPathName(directory)
            except ImportError:
                pass
    except UnicodeError:
        pass
    return directory

def _get_win_folder_with_ctypes(csidl_name):
    ''' Get the folder on windows with the help of ctypes. '''
    import ctypes

    csidl_const = {
        "CSIDL_APPDATA": 26,
        "CSIDL_COMMON_APPDATA": 35,
        "CSIDL_LOCAL_APPDATA": 28,
    }[csidl_name]

    buf = ctypes.create_unicode_buffer(1024)
    ctypes.windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)

    # Downgrade to short path name if have highbit chars. See
    # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
    has_high_char = False
    for char in buf:
        if ord(char) > 255:
            has_high_char = True
            break
    if has_high_char:
        buf2 = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2

    return buf.value


if sys.platform == "win32":
    try:
        import win32com.shell
        _get_win_folder = _get_win_folder_with_pywin32
    except ImportError:
        try:
            import ctypes
            _get_win_folder = _get_win_folder_with_ctypes
        except ImportError:
            _get_win_folder = _get_win_folder_from_registry
