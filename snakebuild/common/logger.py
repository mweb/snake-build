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

from snakebuild.common import config
#from snakebuild.common import filetools


def create_logger():
    ''' Create a default logging information and set the default values.
    '''
    # change this to WARNING but at the moment DEBUG is ok
    # do regreate the logger with the settings in the config
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s %(modules)s [%(lineno)s]: '
                '%(message)s',
        filemode='w')

    __set_logger_default_parameters()
    set_logging_to_config_values()


def set_logging_to_config_values():
    ''' Set the logging to the values specified within the config.
    '''
    __set_log_level_config()
    __set_log_output_config()


def __set_logger_default_parameters():
    ''' Set the default parameters for the logger, it will be added to the main
        application parameters. (application_name)
    '''
    conf = config.Config()
    defaultParameters = {
        'logging_level': ('warning', 'The level of logging messages. '
                                'Possible values are: fatal, critical, '
                                'error, warning, info, debug.',
                    str),
        'logging': ('stdout', 'The output for the logging. Possible values '
                                'are stdout (for console output) file (for '
                                'logging into a file). To use both split the'
                                ' names with a semicolon.',
                    str),
        'logging_dir': ('/var/log/%s' % conf.application_name, 'The directory'
                                ' where to store the logging file. ',
                    str)}

    #conf.set_default_parameters(conf.application_name, defaultParameters)


def __set_log_level_config():
    ''' Set the log level to the current configured value. Possible values are
        fatal    (show only the fatal messages)
        critical (show only the cirtical and the fatal messages)
        error    (show only error, critical and fatal messages)
        warning  (show the warnings and all above messages)
        info     (show the general information and all above messages)
        debug    (show all messages)
    '''
    conf = config.Config()
    logger = logging.getLogger()
    # set the logging level correct
    level = conf.get(conf.application_name, 'logging_level').lower()
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


def __set_log_output_config():
    ''' Set the log output config to the configured value.
    '''
    conf = config.Config()
    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - '
            '%(name)-10s: %(message)s')
    logger = logging.getLogger()
    # set the logging output
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logtype = conf.get(conf.application_name, 'logging').split(';')
    for output in logtype:
        output = output.strip().lower()
        if output == 'stdout':
            # TODO check how to set other than stdout
            handler = logging.StreamHandler()
        elif output == 'file':
            # TODO change this
            filetools.check_dir(conf.get(conf.application_name, 'logging_dir'))
            handler = logging.FileHandler(
                    os.path.join(conf.get(conf.application_name, 'logging_dir'),
                                '%s.log' % conf.application_name))
        elif output == '':
            continue
        else:
#           log.warning('Unsupported log type: %s' % output)
            continue
        handler.setFormatter(formatter)
        logger.addHandler(handler)
