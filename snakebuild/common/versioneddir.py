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
''' This module provides acces to files which are stored within a directory
    that use version control for the files.
    The main goal of this is to be able to get a controlled latest version and
    to add change comments if files change during usage.
'''

import os.path
import sys
import subprocess


class VersionedDirException(BaseException):
    ''' The exception thrown if an error within the VersionedDir class
        occures.
    '''


def get_versioned_directory(directory):
    ''' Get a versioned directory object. It will return an object matching
        the VCS used to store the config files.
        The directory must exist and must be a directory managed by a
        supported VCS (GIT, Mercurial,...)
        Currently onyl GIT is supported.

        @param directory: The directory to load.
        @return: The object to access and update files.
    '''
    if not os.path.isdir(directory):
        raise VersionedDirException('The given directory does not exist: '
                '{0}'.format(directory))


class VersionedGITDir(object):
    ''' This class gives access to the files and helps to select a certain
        version and updating the files.
    '''

    def __init__(self, directory):
        ''' Initialize a given versioned directory. The directory must exist
            and it must contain a valid repository (GIT, SVN, Mercurial,...)
            Not yet all supported.
        '''
        if not os.path.isdir(os.path.join(directory, '.git')):
            raise VersionedDirException('The given directory is not a git'
                    'repository: {0}'.format(directory))
        self.path = directory
        self.prevdir = None

    def update(self, name):
        ''' Make sure that the given file is a the given tag/branch and that
            it is up to date. If there are uncommited changed overwrite them
            with the values from the repository.

            WARNING: Use with caution since this might overwrite manual
                changes.

            @param name: The name of the branch or tag to use for the update.
        '''
        raise VersionedDirException('Not yet implemented.')

    def add_file(self, name):
        ''' Add a new file to the repository to be managed by this repo. This
            does not commit the change, only prepares it.

            @param name: The name of the file to add (path within the
                repository
        '''
        raise VersionedDirException('Not yet implemented.')

    def commit(self, author, comment):
        ''' Commit all open changes within the repository.

            @param author: The name of the author to commit under
            @param comment: The comment to provide with the commmit.
        '''
        raise VersionedDirException('Not yet implemented.')

    def push_remote(self, name):
        ''' Push all the changes to the configured remote repository.

            @param name: The name of the given remote repository.
        '''
        raise VersionedDirException('Not yet implemented.')

    def get_full_path(self, name):
        ''' Get the full path to the file stored within the file.

            @param name: The path within the repository to access.
        '''
        return os.path.join(self.path, name)

    def _git(self, *args):
        ''' call the git command and return the command it self to use the
            stdout, stdin as pipes.

            @*args: The arguments to give to the git command
            @return: The Popen return value
        '''
        self._change_to_repo()

        cmd = subprocess.Popen(['git'] + list(args), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=sys.stderr)

        self._change_back()
        return cmd

    def _gitr(self, *args):
        ''' call the git command and only read the return value. '''
        cmd = self._git(*args)
        stdout, stderr = cmd.communicate()
        return cmd.returncode

    def _change_to_repo(self):
        ''' switch to the current repo directory to call the git commands. '''
        self.prevdir = os.getcwd()
        os.chdir(self.path)

    def _change_back(self):
        ''' switch back to the previous directory. '''
        if self.prevdir is not None:
            os.chdir(self.prevdir)
            self.prevdir = None
