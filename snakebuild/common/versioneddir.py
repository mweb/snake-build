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
import re
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

    if os.path.isdir(os.path.join(directory, '.git')):
        return VersionedGitDir(directory)
    else:
        raise VersionedDirException('The given directory uses no VCS or the '
                'given VCS is not supported. {0}'.format(directory))


class VersionedGitDir(object):
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

    def get_tags(self):
        ''' Get all tag names of the repository. '''
        cmd = self._git('tag')
        stdout, stderr = cmd.communicate()
        tags = [value for value in stdout.split()]
        return tags

    def get_branchs(self):
        ''' Get all tag names of the repository. '''
        cmd = self._git('branch')
        stdout, stderr = cmd.communicate()
        branchs = []
        for value in stdout.split('\n'):
            if value.startswith('*'):
                branchs.append(value[2:].strip())
            elif len(value) > 0:
                branchs.append(value.strip())
        return branchs

    def get_current_branch(self):
        ''' Get the current branch. If currently no branch is selected (not
            ready to commit) None is returned
        '''
        cmd = self._git('branch')
        stdout, stderr = cmd.communicate()
        branchs = [value for value in stdout.split('\n')]
        for branch in branchs:
            if branch.startswith('*') and not branch == "* (no branch)":
                return branch[2:].strip()

        return None

    def get_current_tag(self):
        ''' Get the current tag name if the current repos is on a tag.
            Otherwise None
        '''
        cmd = self._git('describe')
        stdout, stderr = cmd.communicate()
        tag = stdout.strip()
        tags = self.get_tags()
        if tag in tags:
            return tag
        return None

    def update(self, name):
        ''' Make sure that the given file is a the given tag/branch and that
            it is up to date. If there are uncommited changed overwrite them
            with the values from the repository.

            WARNING: Use with caution since this might overwrite manual
                changes.

            @param name: The name of the branch or tag to use for the update.
        '''
        if self._gitr('clean', '-fdx'):
            raise VersionedDirException('Could not clean git repository: {0}'.
                    format(self.path))
        if self._gitr('checkout', name):
            raise VersionedDirException('Could not checkout branch/tag from '
                    'git repository: {0}/{1}'.format(self.path, name))

    def add(self, name):
        ''' Add a new file to the repository to be managed by this repo. This
            does not commit the change, only prepares it.

            @param name: The name of the file to add (path within the
                repository
        '''
        if not os.path.isfile(os.path.join(self.path, name)):
            raise VersionedDirException('File to add to the repository does '
                    'not exist: {0}'.format(name))

        if self.get_current_branch() == None:
            raise VersionedDirException('The current repository is not within '
                    'a valid branch, therefore no add allowed. create a '
                    'branch first.')

        if self._gitr('add', name):
            raise VersionedDirException('File to add to the repository could '
                    'not be added: {0}'.format(name))

    def commit(self, author, comment):
        ''' Commit all open changes within the repository.

            @param author: The name of the author to commit under
            @param comment: The comment to provide with the commmit.
        '''
        pattern_check = re.compile(".*<.*@.*\..*>$")
        if re.match(pattern_check, author) == None:
            raise VersionedDirException('The author name must have the '
                    'following format: NAME <EMAIL> but got: {0}'.
                    format(author))
        if self._gitr('commit', '--author', author, '-m', comment):
            raise VersionedDirException('Could not commit to the repository.')

    def short_log(self, name=None, limit=None):
        ''' Get the short log messages this will be tuples with all the
            messages.
            (Author, Email, Message, Date)

            @param limit: If none then all the history is shown otherwise
                    limit it by the number given: For example use 1 to get
                    only the last commit or 3 for the last 3 commits.
        '''
        params = ['log', '--pretty=format:%an|||%ae|||%s|||%at|||%d']
        if name is not None:
            params.append(name)
        if limit is not None:
            if type(limit) is int:
                params.append('-{0}'.format(limit))
            else:
                raise VersionedDirException('Illegal value for limit use an '
                        'int. {0}'.format(limit))
        cmd = self._git(*params)
        stdout, stderr = cmd.communicate()
        results = []
        for line in stdout.split('\n'):
            results.append([value.strip() for value in line.split('|||')])

        return results

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
