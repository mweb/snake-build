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

from snakebuild.resourceclient.clientcmds import status, details


COMMANDS = {'status': (status, 'Get the status of all configured resources.',
                [], {}),
            'details': (details, 'Get the details about one resource.',
                ['RESOURCE_NAME'], {'RESOURCE_NAME': 'The name of the '
                    'resource to get the detail informations.'})}
