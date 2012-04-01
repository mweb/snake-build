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
''' This module provides access to files which are stored within a directory
    that use version control for the files.
    The main goal of this is to be able to get a controlled latest version and
    to add change comments if files change during usage.
'''

import os.path
import sys
import re
import shutil
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


def create_new_repo(name, local_repos_config):
    ''' Create a new respository on the share/server. This creates a new repos
        to be accessed afterwards from a local repos. For GIT this is a bare
        repos.

        The given name must be unique other wise this function will throw an
        exception.

        @param name: The name of the new repository to create
        @param local_repos_config: The configuration to access the local repos
                to create the new repo (ReposConfig type)
    '''
    if local_repos_config.repo_type == local_repos_config.GIT:
        _create_git_repo(name, local_repos_config.path)
    else:
        raise VersionedDirException('The given VCS type is not supported.')


def clone_repo(name, directory, local_repos_config):
    ''' Clone a given respository to start using it. The repos has to exist.

        @param name: The name of the repos to access
        @param directory: The directory to create
        @param local_repos_config: The configuration to access the local repos
                to clone the repo from (ReposConfig type)
    '''
    if local_repos_config.repo_type == local_repos_config.GIT:
        _clone_git_repo(name, directory, local_repos_config.path)
    else:
        raise VersionedDirException('The given VCS type is not supported.')


class ReposConfig(object):
    ''' The repository config to use for creating or clonig repositories. '''

    # the supported VCS currently only GIT
    GIT, UNKNOWN = range(2)

    def __init__(self, repo_type, path):
        ''' Create the ReposConfig object. Currently on GIT is supported
            @param repo_type: The type of the repository, use the types
                    defined
            @param path: The path where to find the repository.
        '''
        if repo_type >= self.UNKNOWN:
            raise VersionedDirException('The given repository type is '
                    'unknown: {0}'.format(repo_type))
        self.repo_type = repo_type

        if repo_type == self.GIT:
            if not os.path.isdir(path):
                raise VersionedDirException('The given path is not a valid '
                        'path for a local git repos has to be a local '
                        'accessible path: {0}'.format(path))

            if not os.access(path, os.W_OK | os.R_OK):
                raise VersionedDirException('The given path for the bar git '
                        'repos is not writeable: {0}'.format(path))
        self.path = path


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
        self.new_repo = False
        if len(self.get_branchs()) == 0:
            self.new_repo = True

    def get_local_path(self, name):
        ''' Get a file or directory name as the full path to access the file.
            if a nested directory or file needs to be accessed specified a
            list with the path to it.
            To access:
                REPOS/DIR1/FILE1
            Use:
                [DIR1, FILE1]

            @param name: The filename or directory to access
            @return the full path to access the file locally
        '''
        if type(name) is list:
            return os.path.join(self.path, *name)
        return os.path.join(self.path, name)

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

        if self.get_current_branch() == None and not self.new_repo:
            raise VersionedDirException('The current repository is not within '
                    'a valid branch, therefore no add allowed. create a '
                    'branch first.')

        if self._gitr('add', name):
            raise VersionedDirException('File to add to the repository could '
                    'not be added: {0}'.format(name))

    def branch(self, name):
        ''' Create a new branch from the current position (tag, branch). This
            command will make sure that the newly created branch will be
            created on the remote repository and therefore it should be
            accessible for all.

            ATTENTION:
            This commits all local changes to the server.

            @param name: The name of the branch to create
        '''
        if name in self.get_branchs():
            raise VersionedDirException('branch already exists '
                    '{0}'.format(name))

        if self._gitr('branch', name):
            raise VersionedDirException('Could not branch the repository.')

        if self.has_remote():
            if self._gitr('push', 'origin', name):
                raise VersionedDirException('Could not push the branch to the '
                        'central repository.')
            if self._gitr('branch', '-d', name):
                raise VersionedDirException('Could not remove local only '
                        'branch the repository.')
            if self._gitr('checkout', name):
                raise VersionedDirException('Could not checkout the new '
                        'branch.')

    def tag(self, name, author_name, author_email, comment):
        ''' Add a tag to the current position (tag, branch). This creates the
            tag but the push_remote must be called to get it on to the server.

            @param name: The name of the tag
            @param author: The author of the tag
            @param comment: The text for tagging
        '''
        if name in self.get_tags():
            raise VersionedDirException('Tag already exists {0}'.format(name))

        if len(author_name) == 0:
            raise VersionedDirException('The author name can not be empty '
                    'for a tag.')
        _check_email_format(author_email)

        if self._gitr('tag', '-a', name, '-m', comment,
                GIT_COMMITTER_NAME=author_name,
                GIT_COMMITTER_EMAIL=author_email):
            raise VersionedDirException('Could not tag the repository.')
        if self.has_remote():
            if self._gitr('push', '--tag'):
                raise VersionedDirException('Could not push git repository: {0}'.
                        format(self.path))

    def commit(self, author_name, author_email, comment):
        ''' Commit all open changes within the repository.

            @param author_name: The name of the author to use for the commit
            @param author_email: The email address of the author to use for
                    the commit
            @param comment: The comment to provide with the commmit.
        '''
        if author_name is None or len(author_name) == 0:
            raise VersionedDirException('The author name can not be empty '
                    'for a commit.')
        _check_email_format(author_email)
        if self._gitr('commit', '-m', comment, '--author',
                '{0} <{1}>'.format(author_name, author_email),
                GIT_COMMITTER_NAME=author_name,
                GIT_COMMITTER_EMAIL=author_email):
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

    def push_remote(self):
        ''' Push all the changes to the configured remote repository.
        '''
        cmds = ['push']
        if self.new_repo:
            cmds.append('origin')
            cmds.append('master')
            self.new_repo = False

        if self._gitr(*cmds):
            raise VersionedDirException('Could not push git repository: {0}'.
                    format(self.path))

    def pull_remote(self):
        ''' Push all the changes to the configured remote repository.

            @param name: The name of the given remote repository.
        '''
        if self._gitr('pull'):
            raise VersionedDirException('Could not pull git repository: {0}'.
                    format(self.path))

    def get_full_path(self, name):
        ''' Get the full path to the file stored within the file.

            @param name: The path within the repository to access.
        '''
        return os.path.join(self.path, name)

    def has_remote(self):
        ''' Check if the given git repos has a remot repos configured.
        '''
        cmd = self._git('remote')
        stdout, stderr = cmd.communicate()
        if len(stdout.split('\n')) == 1:
            if len(stdout) == 0:
                return False
        return True

    def _git(self, *args, **flags):
        ''' call the git command and return the command it self to use the
            stdout, stdin as pipes.

            @*args: The arguments to give to the git command
            @**flags: The env variables which should be set for this call
            @return: The Popen return value
        '''
        self._change_to_repo()
        env = os.environ.copy()
        if flags is not None and len(flags) > 0:
            env.update(flags)

        cmd = subprocess.Popen(['git'] + list(args), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=sys.stderr, env=env)

        self._change_back()
        return cmd

    def _gitr(self, *args, **flags):
        ''' call the git command and only read the return value.

            @*args: The arguments to give to the git command
            @**flags: The env variables which should be set for this call
            @return: The return value of the command
        '''
        cmd = self._git(*args, **flags)
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


def _check_email_format(email):
    ''' Check if the given name email format is as expected.
        Expected: NAME@DOMAIN

        This method raises an error if it does not match otherwise it
        will return nothing.
    '''
    pattern_check = re.compile(".*@.*\..*$")
    if email is None or re.match(pattern_check, email) == None:
        raise VersionedDirException('The email must have the '
                'following format: NAME@DOMAIN (test@test.com) but got:'
                ' {0}'.format(email))


def _create_git_repo(name, path):
    ''' Create a new bare git respository on the give location.

        The given name must be unique other wise this function will throw an
        exception.

        @param name: The name of the new repository to create
        @param path: The path to where to create the bare repos
    '''
    if not os.path.isdir(path):
        raise VersionedDirException('The given path for the git repos does '
                'not exist: {0}'.format(path))
    if not os.access(path, os.W_OK | os.R_OK):
        raise VersionedDirException('The given path for the bare git '
                'repos is not read/writeable: {0}'.format(str(path)))

    if os.path.exists(os.path.join(path, '{0}.git'.format(name))):
        raise VersionedDirException('The given git repo already exists within '
                'the path as a file or directory: {0}'.format(
                os.path.join(path, name)))
    if os.path.exists(os.path.join(path, name)):
        raise VersionedDirException('The temporary directory for the git '
                'repository alread exists: {0}'.format(
                os.path.join(path, name)))

    os.mkdir(os.path.join(path, "{0}.git".format(name)))
    prevdir = os.getcwd()
    os.chdir(os.path.join(path, "{0}.git".format(name)))
    cmd = subprocess.Popen(['git', 'init', '--bare'], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=sys.stderr)
    stdout, stderr = cmd.communicate()
    os.chdir(prevdir)

    if cmd.returncode != 0:
        raise VersionedDirException('Could not initialize git repos: {0}'.
                format(os.path.join(path, name)))

#    cmd = subprocess.Popen(['git', '--bare', 'clone', os.path.join(path, name),
#            os.path.join(path, '{0}.git'.format(name))], stdin=subprocess.PIPE,
#            stdout=subprocess.PIPE, stderr=sys.stderr)
#    stdout, stderr = cmd.communicate()
#
#    if cmd.returncode != 0:
#        raise VersionedDirException('Could not initialize bare git repos: {0}'.
#                format(os.path.join(path, name)))
#
#    shutil.rmtree(os.path.join(path, name))
#

def _clone_git_repo(name, directory, path):
    ''' Create a clone from a given central git repository.

        @param name: The name of the repository to clone
        @param directory: The directory to create
        @param path: The path where the bare git repos is stored
    '''
    if not os.path.isdir(os.path.join(path, '{0}.git'.format(name))):
        raise VersionedDirException('The given bare repo does not exist: '
                '{0}'.format(os.path.join(path, '{0}.git'.format(name))))
    if os.path.exists(directory):
        raise VersionedDirException('The target directory already exists: '
                '{0}'.format(directory))

    cmd = subprocess.Popen(['git', 'clone', os.path.join(path,
            '{0}.git'.format(name)), directory], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=sys.stderr)
    stdout, stderr = cmd.communicate()

    if cmd.returncode != 0:
        raise VersionedDirException('Could not clone bare git repos: {0}'.
                format(os.path.join(path, name)))
