# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2012 Mathias Weber <mathew.weber@gmail.com>
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
''' The webserver implementation for the resourceviewer.
'''

import snakebuild.web as web

import urlhandlers


class WebServer(object):
    ''' The simple webserver starter this server should only be used for local
        test servers and some small installations.
    '''

    def __init__(self, config):
        ''' Initialize the WebServer, perpare anything to run but do not start
            here since this object should be used with the Daemon class.

            @param config: The config object to use
        '''
        self.config = config

        name = "resourceviewer"
        self.pidfile = '/tmp/snakebuild/%s.pid' % name
        self.stdin = '/tmp/snakebuild/%sstdin' % name
        self.stdout = '/tmp/snakebuild/%sstdout' % name
        self.stderr = '/tmp/snakebuild/%sstderr' % name

    def run(self):
        ''' Start the web server. This method does not return until the server
            gets stopped.
        '''
        app = web.application(urlhandlers.urls, globals())

        host = self.config.get_s('resourceviewer', 'hostname')
        port = self.config.get_s('resourceviewer', 'port')
        # this is a rather ugly hack to get web.py working locally (shoult
        # only be used for development. there fore this is fine.
        import sys
        sys.argv[1] = host
        sys.argv.append(port)
        app.run()

    def shutdown(self):
        ''' Stop the server '''
        pass
