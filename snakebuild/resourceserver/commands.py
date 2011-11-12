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
''' This files contains the dictionary with all the commands that the resrouce
    server supports via the network connection.
'''


def _test(cmd, params, config):
    ' This is a test command only used for testing new commands. '''
    print "CMD: %s" % cmd
    print "options: %s" % params

    return 10


COMMANDS = {'test': (_test, 'example', ['test', '[test2]'],
                {'test': 'bla bla',
                '[test2]': 'Ihaaaa'})}
