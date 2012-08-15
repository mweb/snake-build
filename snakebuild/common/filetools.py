# -*- coding: utf-8 -*-
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
''' This module provides some basic helper tools to handle files. '''

import os


def tail(ofile, lines=10, bufsize=1024):
    ''' Get the number of last lines of a file. Usefull for parsing log files.

        @param ofile: The file object to read
        @param lines: The number of lines to return

        @return: a list with all the last lines of the file
    '''
    ofile.seek(0, os.SEEK_END)
    size_bytes = ofile.tell()
    result_lines = []
    while len(result_lines) < lines and size_bytes > 0:
        if (size_bytes - bufsize > 0):
            # go back the size of the buffer
            ofile.seek(-bufsize, os.SEEK_CUR)
            data = ofile.read(bufsize)
            ofile.seek(-bufsize, os.SEEK_CUR)
        else:
            ofile.seek(0, os.SEEK_SET)
        result_lines = data.splitlines() + result_lines
        size_bytes -= bufsize

    return result_lines[-lines:]


def read_full_line(ofile):
    ''' Get the last line from a file, but only if the line ends with a line
        feed, otherwise reest the read pointer.

        @param ofile: The file object to read
    '''
    where = ofile.tell()
    line = ofile.readline()
    if not line:
        return None
    if line.endswith('\n'):
        return line
    ofile.seek(where)
    return None
