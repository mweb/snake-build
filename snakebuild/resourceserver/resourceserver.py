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
''' This file provides a start_server method to start the ResourceServer.
'''

import logging
import os.path

from snakebuild.i18n import _
from snakebuild.common import Daemon
from snakebuild.common.versioneddir import VersionedDirException, ReposConfig,\
        remote_repo_existing, create_new_repo, clone_repo, \
        get_versioned_directory
from snakebuild.communication import Server
from snakebuild.resourceserver.servercommands import COMMANDS
from snakebuild.resourceserver.servercmds import *
from snakebuild.resourceserver.resource import ResourceManager


LOG = logging.getLogger('snakebuild.resourceserver.resourceserver')


def start_server(options, arguments, config):
    ''' Start the resource server.

        @param options: the options set via the command line parameters
        @param config: the global configuration to use for starting the server
        @param arguments: the arguments for the command the first argument
                within this list is always the command it self.
        @return true or false depends on success or failure
    '''
    stop = False
    if not (len(arguments) == 0 or len(arguments) == 1):
        print(_("Could not start the resource server illegal arguments. "
                "Expected None or one argument but got: {0:d}").format(
                len(arguments)))
        return False

    if len(arguments) == 1:
        cmd = arguments[0].lower()
        if cmd == 'stop':
            stop = True
        elif cmd == 'start':
            stop = False
        else:
            print _("Command not supported for starting: {0}").format(
                    arguments[0])

    host = config.get_s('resourceserver', 'hostname')
    port = config.get_s('resourceserver', 'port')
    name = 'resourceserver'

    if stop:
        Daemon(Server(host, port, COMMANDS, name), Daemon.STOP)
    else:
        repos_name = config.get_s('resourceserver', 'resource_repos_name')
        repos_type = config.get_s('resourceserver', 'repository_type')
        repos_data = config.get_s('resourceserver', 'repository_data')
        repos_local = config.get_s('resourceserver', 'repository_local')

        try:
            repos_config = ReposConfig(repos_type, repos_data)
        except VersionedDirException, exc:
            LOG.error('The given repository type and repository data are '
                    'invalid. Fix the configuration: {0}'.format(str(exc)))

        if os.path.isdir(os.path.join(repos_local, repos_name)):
            versioned_dir = get_versioned_directory(os.path.join(repos_local,
                    repos_name))
        else:
            if not remote_repo_existing(repos_name, repos_config):
                create_new_repo(repos_name, repos_config)
            path = os.path.join(repos_local, repos_name)
            clone_repo(repos_name, path, repos_config)
            versioned_dir = get_versioned_directory(path)

        # TODO use versioned dir (and tag to use)
        resourcemanager = ResourceManager(versioned_dir)
        if options.background:
            Daemon(Server(host, port, COMMANDS, name, resourcemanager),
                    Daemon.START)
        else:
            Daemon(Server(host, port, COMMANDS, name, resourcemanager),
                    Daemon.FOREGROUND)

    return True
