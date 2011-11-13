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
''' This file holds functions for configuring the logger.
'''

import logging
import os


def create_logger(config, appname=None):
    ''' Create a default logging information and set the default values.

        @param config: The config instance to load
        @param appname: The key name of the app to get the config for. If not
            set then then the application name of the config is taken
    '''
    # change this to WARNING but at the moment DEBUG is ok
    # do regreate the logger with the settings in the config
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s %(modules)s [%(lineno)s]: '
                '%(message)s',
        filemode='w')

    set_logging_to_config_values(config, appname)


def set_logging_to_config_values(config, appname=None):
    ''' Set the logging to the values specified within the config.

        @param config: The config instance to load
        @param appname: The key name of the app to get the config for. If not
            set then then the application name of the config is taken
    '''
    if appname is None:
        appname = config.application_name

    __set_log_level_config(config, appname)
    __set_log_output_config(config, appname)


def __set_log_level_config(config, appname):
    ''' Set the log level to the current configured value. Possible values are
        fatal    (show only the fatal messages)
        critical (show only the cirtical and the fatal messages)
        error    (show only error, critical and fatal messages)
        warning  (show the warnings and all above messages)
        info     (show the general information and all above messages)
        debug    (show all messages)

        @param config: The config instance to get the settings from
        @param appname: The key name of the app to get the config for.
    '''
    logger = logging.getLogger()
    # set the logging level correct
    level = config.get_s(appname, 'logging_level').lower()
    if level == 'critical':
        logger.setLevel(logging.CRITICAL)
    elif level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif level == 'error':
        logger.setLevel(logging.ERROR)
    elif level == 'fatal':
        logger.setLevel(logging.FATAL)
    elif level == 'warning':
        logger.setLevel(logging.WARNING)
    elif level == 'info':
        logger.setLevel(logging.INFO)


def __set_log_output_config(config, appname):
    ''' Set the log output config to the configured value.

        @param config: The config instance to get the settings from
        @param appname: The key name of the app to get the config for.
    '''
    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - '
            '%(name)-10s: %(message)s')
    logger = logging.getLogger()
    # set the logging output
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logtype = config.get_s(appname, 'logging').split(';')
    for output in logtype:
        output = output.strip().lower()
        if output == 'stdout':
            # TODO check how to set other than stdout
            handler = logging.StreamHandler()
        elif output == 'file':
            # TODO change this
            #filetools.check_dir(conf.get_s(appname, 'logging_dir'))
            handler = logging.FileHandler(
                    os.path.join(config.get_s(appname, 'logging_dir'),
                                '%s.log' % appname))
        elif output == '':
            continue
        else:
#           log.warning('Unsupported log type: %s' % output)
            continue
        handler.setFormatter(formatter)
        logger.addHandler(handler)
