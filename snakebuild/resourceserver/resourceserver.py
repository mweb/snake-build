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
from snakebuild.common import Daemon, output
from snakebuild.common.versioneddir import VersionedDirException, \
        ReposConfig, remote_repo_existing, create_new_repo, clone_repo, \
        get_versioned_directory
from snakebuild.commands import handle_cmd
from snakebuild.communication import Server
from snakebuild.resourceserver.servercmds import *
from snakebuild.resourceserver.resource import ResourceManager
from snakebuild.resourceserver.commandlineparser import command, SHELL_COMMANDS


LOG = logging.getLogger('snakebuild.resourceserver.resourceserver')


def start_server(arguments, config):
    ''' Start the resource server.

        @param config: the global configuration to use for starting the server
        @param arguments: the arguments given to the command.
        @return true or false depends on success or failure
    '''
    try:
        return handle_cmd(SHELL_COMMANDS, arguments, config)
    except KeyboardInterrupt:
        output.error(_('Abort by keyboard interrupt.'))
        return False


@command('stop', (
    (('--name',), {'help': _('The name of the resourceserver to stop.'),
        'default': 'resourceserver'}),
    ))
def stop_server(args, config):
    ''' Stop the resource server.

        @param args: The arguments provided with the command
        @param config: The config object to use

        @return true or false depends on success or failure
    '''
    host = config.get_s('resourceserver', 'hostname')
    port = config.get_s('resourceserver', 'port')

    Daemon(Server(host, port, args.name), Daemon.STOP)
    return True


@command('start', (
    (('--background',), {'action': 'store_true',
        'help': _('Run the build agent as a daemon (background)'),
        'default': False}),
    (('--tag',), {'default': 'master', 'help': _('specify the git tag to use '
        'to read the config of the server.')}),
    (('--name',), {'help': _('The name of the agent to start. This name '
        'has to be unique on one server.'), 'default': 'resourceserver'})
    ))
def start_server_now(args, config):
    ''' Start the resource server.

        @param args: The arguments provided with the command
        @param config: The config object to use

        @return true or false depends on success or failure
    '''
    host = config.get_s('resourceserver', 'hostname')
    port = config.get_s('resourceserver', 'port')
    name = 'resourceserver'

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

    if args.tag is not None:
        versioned_dir.update(args.tag)
    else:
        # if nothing is specified always go for the master
        versioned_dir.update("master")

    resourcemanager = ResourceManager(versioned_dir)
    if args.background:
        Daemon(Server(host, port, name, resourcemanager),
                Daemon.START)
    else:
        Daemon(Server(host, port, name, resourcemanager),
                Daemon.FOREGROUND)

    return True
