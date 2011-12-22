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
''' The function within this file support the output to the console file or any
    other source which requires pretty printed output.
'''

import os

from snakebuild.i18n import _

__LINE_LENGTH = None


def message(value, indent="", line_length=None, first_indent=None):
    ''' print a message to the standard out. It uses thes format message to
        format the message see the format_message function for the detailed
        description of the parameters.
    '''
    print format_message(value, indent, line_length, first_indent)


def error(value, line_length=None):
    ''' print a error message io the standard out. '''
    print format_message(_("Error: {0}").format(value), indent=" " * 4,
            line_length=line_length, first_indent="")


def warning(value, line_length=None):
    ''' print a warning message io the standard out. '''
    print format_message(_("Warning: {0}").format(value), indent=" " * 4,
            line_length=line_length, first_indent=0)


def format_message(value, indent="", line_length=None, first_indent=None):
    ''' Return a string with newlines so that the given string fits into this
        line length. At the start of the line the indent is added. This can
        be used for commenting the message out within a file or to indent your
        text.

        If the line length is set to None then the width is expected to be the
        width of the current console.
        All \\t will be replaced with 4 spaces.

        @param value: The string to get as a commented multiline comment.
        @param indent: The indent to use for printing or charcter to put in
                front
        @param line_length: The length of the line to fill. (default None)
        @param first_indent: The first indent might be shorter. If None then
                the first line uses the normal indent as the rest of the
                string.

        @return: The string with newlines
    '''
    if indent.find('\t'):
        indent = indent.replace('\t', '    ')
    line_length = get_line_length(line_length)

    result = []
    if first_indent is None:
        first_indent = indent
    cindent = first_indent
    tmp = "*" * line_length
    for ele in value.split(' '):
        if ele.find('\t') >= 0:
            ele = ele.replace('\t', '    ')
        if (len(ele) + len(tmp)) >= line_length:
            result.append(tmp)
            tmp = '{0}{1}'.format(cindent, ele)
            cindent = indent
        else:
            tmp = "{0} {1}".format(tmp, ele)
    result.append(tmp)
    result = result[1:]
    return "\n".join(result)


def get_line_length(line_length):
    ''' Get the line length of a terminal or the given line lenght if not None

        @param line_length: The line length to chekc if None then the terminal
                width is returned
        @return the length of the line to use for the current terminal.
    '''
    if line_length is not None:
        return line_length

    global __LINE_LENGTH
    if __LINE_LENGTH is None:
        __LINE_LENGTH = _get_terminal_size()[0] - 1
    return __LINE_LENGTH


def _get_terminal_size():
    ''' Get the size of the current terminal.

        @return: (width, height)
    '''
    def ioctl_get_win_size(fdr):
        ''' try to get the size of a terminal
            @param fdr: The filedescriptor id
        '''
        try:
            import fcntl
            import termios
            import struct
            crr = struct.unpack('hh',
                    fcntl.ioctl(fdr, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return crr
    crr = (ioctl_get_win_size(0) or ioctl_get_win_size(1) or
            ioctl_get_win_size(2))
    if not crr:
        try:
            fdr = os.open(os.ctermid(), os.O_RDONLY)
            crr = ioctl_get_win_size(fdr)
            os.close(fdr)
        except:
            pass
    if not crr:
        try:
            crr = (env['LINES'], env['COLUMNS'])
        except:
            # safe default value (we take 80 here)
            crr = (25, 80)

    return int(crr[1]), int(crr[0])
