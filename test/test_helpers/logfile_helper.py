#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2012 Mathias Weber <mathew.weber@gmail.com>
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
#
''' Some helper functions for testing with the help of a log file. '''

import logging
import tempfile


def prepare_log_file():
    """ Setup the logger to log into a temporaly created file. This
        function sets up a new file handler to log all messages to the
        given file.

        The file has to be removed by the user of this function

        :returns: the filename full path
    """
    f, logfile = tempfile.mkstemp(".log")

    logger = logging.getLogger()
    # remove all other log handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)

    handler = logging.FileHandler(logfile)
    logger.addHandler(handler)

    return logfile


def check_log_file(filename, string):
    """ Search for the given string in a log file. Return True if available
        and False if not available.

        :filename: The log file to check
        :string: The string to search for
        :returns: True if string was found and False if the string wasn't found
    """
    logf = open(filename, 'r')
    for line in logf.readlines():
        if line.find(string) >= 0:
            return True

    return False
