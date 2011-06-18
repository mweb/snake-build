# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

''' THIS IS snakebuild_resourceserver-common CONFIGURATION FILE
    YOU CAN PUT THERE SOME GLOBAL VALUE
    Do not touch unless you know what you're doing.
    you're warned :)
'''

__all__ = [
    'ProjectPathNotFound',
    'get_data_file',
    'get_config_file',
    'get_data_path',
    'get_config_path',
    ]

# Where your project will look for your data (for instance, images and ui
# files). By default, this is ../data, relative your trunk layout
__snakebuild_resourceserver_data_directory__ = '../data/'
__snakebuild_resourceserver_config_directory__ = '../etc/'
__license__ = 'Mathias Weber, 2006-2011'

import os

import gettext
#from gettext import gettext as _
gettext.textdomain('snakebuild_resourceserver')


class ProjectPathNotFound(Exception):
    """Raised when we can't find the project directory."""
    pass


def get_data_file(*path_segments):
    """Get the full path to a data file.

    Returns the path to a file underneath the data directory (as defined by
    `get_data_path`). Equivalent to os.path.join(get_data_path(),
    *path_segments).
    """
    return os.path.join(get_data_path(), *path_segments)


def get_config_file(*path_segments):
    """Get the full path to a config file.

    Returns the path to a file underneath the config directory (as defined by
    `get_config_path`). Equivalent to os.path.join(get_config_path(),
    *path_segments).
    """
    return os.path.join(get_config_path(), *path_segments)


def get_data_path():
    """Retrieve snakebuild_resourceserver data path

    This path is by default <snakebuild_resourceserver_lib_path>/../data/ in
    trunk and /usr/share/snakebuild_resourceserver_common in an installed
    version but this path is specified at installation time.
    """

    # Get pathname absolute or relative.
    if __snakebuild_resourceserver_data_directory__.startswith('/'):
        path = __snakebuild_resourceserver_data_directory__
    else:
        path = os.path.join(os.path.dirname(__file__),
                __snakebuild_resourceserver_data_directory__)

    abs_data_path = os.path.abspath(path)
    if not os.path.exists(abs_data_path):
        raise ProjectPathNotFound

    return abs_data_path


def get_config_path():
    """Retrieve snakebuild_resourceserver config path

    This path is by default
    <snakebuild_resourceserver_lib_path>/../etc/snakebuild
    in trunk and /etc/snakebuild in an installed version but this path is
    specified at installation time.
    """

    # Get pathname absolute or relative.
    if __snakebuild_resourceserver_config_directory__.startswith('/'):
        path = __snakebuild_resourceserver_config_directory__
    else:
        path = os.path.join(os.path.dirname(__file__),
            __snakebuild_resourceserver_config_directory__, 'snakebuild')

    abs_data_path = os.path.abspath(path)
    if not os.path.exists(abs_data_path):
        raise ProjectPathNotFound
    return abs_data_path
