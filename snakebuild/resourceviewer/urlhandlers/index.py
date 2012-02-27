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
''' All the classes for handling the urls within the viewer.
'''

import snakebuild.web as web

from snakebuild.i18n import _
from snakebuild.common import output
from snakebuild.communication import ClientCommunicationException
from snakebuild.resourceclient.servercmds import ResourceServer, \
        ResourceServerRemoteError


class index(object):
    ''' This class is used as the index page. '''

    def GET(self):
        ''' handle the get request of the webserver '''

        srvr = ResourceServer('localhost', 4224)
        try:
            answer = srvr.get_status_list()
        except ResourceServerRemoteError, exc:
            output.error(_("Got error while talking with the server:\n "
                    "{0}").format(exc))
            return "ERROR"
        except ClientCommunicationException, exc:
            output.error(exc)
            return "ERROR"

        renderer = web.template.render('data/templates/resourceview/',
                base="base")
        return renderer.content('test', answer)
