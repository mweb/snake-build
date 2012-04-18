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
''' The snakebuild build agent instance that does all the building. '''


class BuildAgent(object):
    ''' This is the BuildAgent object which runs a given script step by step.

        The build steps need to be stored within a versioned directory that
        this agent checks out before running them. This way we always have a
        clean environment to build.
        The Information about the version use to build will always be stored
        that we are able to run the same build again.
    '''
    IDLE, STARTING, RUNNING, WAITING, FINISH = range(5)

    def __init__(self, repository_config):
        ''' Create the BuildAgent object.
        '''
        self.is_running = False
        self.repository_config = repository_config

    def start_build(self, job_name, version_name):
        ''' Start a build.

            @param job_name: The name of the job to build (the name of the
                    repository on the remote location.)
            @param version_name: The name of the version to use for building
                    this is might be the tag or branch name

            @return: True on success (job got started), False on error
        '''
        return True

    def status(self):
        ''' Get the current status of the agent. If it is building then get
            the current job step and if there where any errors or warnings.

            @return STATUS
        '''
        return self.is_running
