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
''' This files contains the dictionary with all the commands which are
    supported by the resource client command.
'''

from snakebuild.communication.client import Client


def _test(cmd, options, config, example, example2=None):
    ' This is a test command only used for testing new commands. '''
    print "CMD: %s" % cmd
    print "options: %s" % options
    print "Examples: %s" % example
    print "Example2: %s" % example2

    cl = Client('localhost', 4224)

    answ = cl.send(Client.SJSON, 'test', (12, 13))

    print answ


COMMANDS = {'acquire': (_test, 'example', ['test', '[test2]'],
                {'test': 'bla bla',
                '[test2]': 'Ihaaaa'})}
