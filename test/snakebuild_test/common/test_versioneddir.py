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
''' The unit test for the versioned directory class '''

import unittest
import os
import stat
import time
import shutil
import subprocess

import snakebuild.common.versioneddir as vd
from snakebuild.common.appdirs import tmp_data_dir


class TestVersionedDir(unittest.TestCase):
    ''' The unit test for the snake build common versioned dir classes. '''
    def setUp(self):
        ''' Setup the test case. '''
        self.tempgitdir = os.path.join(tmp_data_dir(), 'snakebuild_git_test')
        self.tempnonedir = os.path.join(tmp_data_dir(), 'snakebuild_none_test')

        if os.path.isdir(self.tempgitdir):
            shutil.rmtree(self.tempgitdir)
        if os.path.isdir(self.tempnonedir):
            shutil.rmtree(self.tempnonedir)

        os.makedirs(self.tempgitdir)
        os.makedirs(self.tempnonedir)
        _init_git_repo(self.tempgitdir)

    def test_init(self):
        ''' Test the initialisation of a new versioned directory.
        '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        self.assertTrue(type(versioned) is vd.VersionedGitDir)
        self.assertTrue(versioned.get_full_path('one') ==
                os.path.join(self.tempgitdir, 'one'))

        with self.assertRaises(vd.VersionedDirException):
            versioned = vd.get_versioned_directory(self.tempnonedir)

        with self.assertRaises(vd.VersionedDirException):
            versioned = vd.get_versioned_directory(os.path.join(
                    self.tempnonedir, 'munchkin'))

        with self.assertRaises(vd.VersionedDirException):
            versioned = vd.VersionedGitDir(self.tempnonedir)

    def test_get_branchs_command(self):
        ''' Test the get_branchs command. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        branchs = versioned.get_branchs()

        self.assertTrue(len(branchs) == 2)
        self.assertTrue('master' in branchs)
        self.assertTrue('v1.x' in branchs)

    def test_get_tags_command(self):
        ''' Test the get_tags command. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        tags = versioned.get_tags()
        self.assertTrue(len(tags) == 3)
        self.assertTrue('v1.0' in tags)
        self.assertTrue('v1.1' in tags)
        self.assertTrue('v2.0' in tags)

    def test_get_current_branch(self):
        ''' Test getting the current branch. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        self.assertTrue(versioned.get_current_branch() == 'master')

        versioned._gitr('checkout', 'v1.x')
        self.assertTrue(versioned.get_current_branch() == 'v1.x')

        versioned._gitr('checkout', 'v1.0')
        self.assertTrue(versioned.get_current_branch() == None)

        versioned._gitr('checkout', 'master')
        self.assertTrue(versioned.get_current_branch() == 'master')

    def test_get_current_tag(self):
        ''' Test getting the current tag name. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        self.assertTrue(versioned.get_current_tag() == 'v2.0')

        versioned._gitr('checkout', 'v1.x')
        self.assertTrue(versioned.get_current_tag() == None)

        versioned._gitr('checkout', 'v1.1')
        self.assertTrue(versioned.get_current_tag() == 'v1.1')

        versioned._gitr('checkout', 'v1.0')
        self.assertTrue(versioned.get_current_tag() == 'v1.0')

        versioned._gitr('checkout', 'master')
        self.assertTrue(versioned.get_current_tag() == 'v2.0')

    def test_update(self):
        ''' Test if the update command works as expected '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        self.assertTrue(versioned.get_current_tag() == 'v2.0')
        versioned.update('v2.0')
        self.assertTrue(versioned.get_current_tag() == 'v2.0')
        versioned.update('master')
        self.assertTrue(versioned.get_current_branch() == 'master')

        versioned.update('v1.x')
        self.assertTrue(versioned.get_current_tag() == None)
        self.assertTrue(versioned.get_current_branch() == 'v1.x')

        versioned.update('v1.1')
        self.assertTrue(versioned.get_current_tag() == 'v1.1')

        with self.assertRaises(vd.VersionedDirException):
            versioned.update('1234')

        demofile = open(os.path.join(self.tempgitdir, 'kk'), 'w')
        demofile.write('demo')
        demofile.close()

        self.assertTrue(os.path.isfile(os.path.join(self.tempgitdir, 'kk')))
        versioned.update('master')
        self.assertFalse(os.path.isfile(os.path.join(self.tempgitdir, 'kk')))

    def test_add_commmit(self):
        ''' Test the add and the commit methods. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)

        with self.assertRaises(vd.VersionedDirException):
            versioned.add('test.out')

        with self.assertRaises(vd.VersionedDirException):
            versioned.commit('Tester <test@test.com>', 'test commit')

        demofile = open(os.path.join(self.tempgitdir, 'test.out'), 'w')
        demofile.write('demo')
        demofile.close()

        versioned.add('test.out')
        with self.assertRaises(vd.VersionedDirException):
            versioned.commit('Tester <test@test>', 'test commit')
        with self.assertRaises(vd.VersionedDirException):
            versioned.commit('Tester <test@test.com>asdf', 'test commit')
        with self.assertRaises(vd.VersionedDirException):
            versioned.commit('Tester', 'test commit')
        versioned.commit('Tester <test@test.com>', 'test commit')

        # check log messages
        cmd = versioned._git('log', "--pretty=format:%an", '-1')
        stdout, stderr = cmd.communicate()
        self.assertTrue(stdout == 'Tester')
        cmd = versioned._git('log', "--pretty=format:%ae", '-1')
        stdout, stderr = cmd.communicate()
        self.assertTrue(stdout == 'test@test.com')
        cmd = versioned._git('log', "--pretty=format:%s", '-1')
        stdout, stderr = cmd.communicate()
        self.assertTrue(stdout == 'test commit')

        # add file to tag (not allowed)
        versioned.update('v1.0')
        demofile = open(os.path.join(self.tempgitdir, 'test.out'), 'w')
        demofile.write('demo')
        demofile.close()

        with self.assertRaises(vd.VersionedDirException):
            versioned.add('test.out')
        with self.assertRaises(vd.VersionedDirException):
            versioned.commit('Tester <test@test.com>', 'test commit')

        # add file to branche (allowed)
        versioned.update('v1.x')
        demofile = open(os.path.join(self.tempgitdir, 'test.out'), 'w')
        demofile.write('demo')
        demofile.close()

        versioned.add('test.out')
        versioned.commit('Tester <test@test.com>', 'test commit')

    def test_short_log_command(self):
        ''' Test the short log command to get a short log message. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        logs = versioned.short_log(limit=1)
        self.assertTrue(len(logs) == 1)
        self.assertTrue(len(logs[0]) == 5)

        # this might change if we change something on the setup and might be
        # different for other repos types this currently only works for git
        logs = versioned.short_log()
        self.assertTrue(len(logs) == 3)

        # add file with given author to check history
        demofile = open(os.path.join(self.tempgitdir, 'test.out'), 'w')
        demofile.write('demo')
        demofile.close()

        versioned.add('test.out')
        versioned.commit('Tester <test@test.com>', 'test commit')

        logs = versioned.short_log(limit=1)
        self.assertTrue(len(logs) == 1)
        self.assertTrue(logs[0][0] == 'Tester')
        self.assertTrue(logs[0][1] == 'test@test.com')
        self.assertTrue(logs[0][2] == 'test commit')
        self.assertTrue(int(logs[0][3]) < time.time())
        self.assertTrue(logs[0][4] == "(HEAD, master)")

        # test illegal value for history length
        with self.assertRaises(vd.VersionedDirException):
            logs = versioned.short_log(limit='1')
        with self.assertRaises(vd.VersionedDirException):
            logs = versioned.short_log(limit=1.12)

    def test_short_log_command_for_file(self):
        ''' Test the short log command to get a short log message. '''
        versioned = vd.get_versioned_directory(self.tempgitdir)
        logs = versioned.short_log("one")
        self.assertTrue(len(logs) == 1)
        self.assertTrue(len(logs[0]) == 5)

        # add file with given author to check history
        demofile = open(os.path.join(self.tempgitdir, 'test.out'), 'w')
        demofile.write('demo')
        demofile.close()

        versioned.add('test.out')
        versioned.commit('Tester <test@test.com>', 'test commit')

        logs = versioned.short_log("test.out")
        self.assertTrue(len(logs) == 1)
        self.assertTrue(logs[0][0] == 'Tester')
        self.assertTrue(logs[0][1] == 'test@test.com')
        self.assertTrue(logs[0][2] == 'test commit')
        self.assertTrue(int(logs[0][3]) < time.time())
        self.assertTrue(logs[0][4] == "(HEAD, master)")

        # change file with given author to check history
        demofile = open(os.path.join(self.tempgitdir, 'test.out'), 'w')
        demofile.write('demo2go')
        demofile.close()

        versioned.add('test.out')
        versioned.commit('Tester <test@test.com>', 'test commit')
        logs = versioned.short_log("test.out")
        self.assertTrue(len(logs) == 2)
        for log in logs:
            self.assertTrue(log[0] == 'Tester')
            self.assertTrue(log[1] == 'test@test.com')
            self.assertTrue(log[2] == 'test commit')
            self.assertTrue(int(log[3]) < time.time())

        self.assertTrue(logs[0][4] == "(HEAD, master)")
        self.assertTrue(logs[1][4] == "")

        logs = versioned.short_log("test.out", 1)
        self.assertTrue(len(logs) == 1)

    def test_git_push_pull_commands(self):
        ''' Test if the interaction with the remote git repository works. '''
        baredir = os.path.join(os.path.dirname(self.tempgitdir),
                'snakebuild_git_test_bare.git')
        clonedir1 = os.path.join(os.path.dirname(self.tempgitdir),
                'snakebuild_git_test_clone1')
        clonedir2 = os.path.join(os.path.dirname(self.tempgitdir),
                'snakebuild_git_test_clone2')

        _create_clone(self.tempgitdir, baredir, True)
        _create_clone(baredir, clonedir1)
        _create_clone(baredir, clonedir2)

        clone1 = vd.get_versioned_directory(clonedir1)
        clone2 = vd.get_versioned_directory(clonedir2)

        demofile = open(os.path.join(clonedir1, 'clone1.out'), 'w')
        demofile.write('demo')
        demofile.close()
        clone1.add('clone1.out')
        clone1.commit('Tester <test@test.com>', 'test clone1 commit')
        clone1.push_remote()

        demofile = open(os.path.join(clonedir2, 'clone2.out'), 'w')
        demofile.write('demo')
        demofile.close()
        clone2.add('clone2.out')
        clone2.commit('Tester <test@test.com>', 'test clone1 commit')
        with self.assertRaises(vd.VersionedDirException):
            clone2.push_remote()
        clone2.pull_remote()
        clone2.push_remote()

        self.assertTrue(os.path.isfile(os.path.join(clonedir2, 'clone1.out')))

        self.assertFalse(os.path.isfile(os.path.join(clonedir1, 'clone2.out')))
        clone1.pull_remote()
        self.assertTrue(os.path.isfile(os.path.join(clonedir1, 'clone2.out')))

        shutil.rmtree(baredir)
        with self.assertRaises(vd.VersionedDirException):
            clone1.pull_remote()
        with self.assertRaises(vd.VersionedDirException):
            clone1.push_remote()

    def test_git_commands(self):
        ''' Test the internal git command methods.
        '''
        versioned = vd.VersionedGitDir(self.tempgitdir)
        self.assertTrue(versioned._gitr('branch') == 0)

    def test_repos_config(self):
        ''' Test the ReposConfig class if it works as expected. '''
        tmpname = os.path.join(tmp_data_dir(), 'snakebuild_test')
        if os.path.exists(tmpname):
            shutil.rmtree(tmpname)

        rconf = vd.ReposConfig(vd.ReposConfig.GIT, tmp_data_dir())
        self.assertTrue(rconf.path == tmp_data_dir())
        self.assertTrue(rconf.repo_type == vd.ReposConfig.GIT)

        rconf = vd.ReposConfig(vd.ReposConfig.GIT, os.path.abspath('.'))
        self.assertTrue(rconf.path == os.path.abspath('.'))
        self.assertTrue(rconf.repo_type == vd.ReposConfig.GIT)

        with self.assertRaises(vd.VersionedDirException):
            rconf = vd.ReposConfig(vd.ReposConfig.GIT,
                    os.path.join(tmp_data_dir(), 'not_existing'))

        with self.assertRaises(vd.VersionedDirException):
            rconf = vd.ReposConfig(vd.ReposConfig.UNKNOWN, tmp_data_dir())

        with self.assertRaises(vd.VersionedDirException):
            rconf = vd.ReposConfig(vd.ReposConfig.UNKNOWN + 1, tmp_data_dir())

        os.makedirs(tmpname)
        os.chmod(tmpname, stat.S_IRUSR)

        # test with not writeable repository directory
        with self.assertRaises(vd.VersionedDirException):
            rconf = vd.ReposConfig(vd.ReposConfig.GIT, tmpname)

        os.chmod(tmpname, stat.S_IRUSR | stat.S_IWUSR)
        shutil.rmtree(tmpname)

    def test_create_git_repos(self):
        ''' Test the _create_git_repo function '''
        barename = os.path.join(tmp_data_dir(), 'snakebuild_git_test_bare')
        if os.path.isdir(barename):
            shutil.rmtree(barename)
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))

        vd._create_git_repo('snakebuild_git_test_bare', tmp_data_dir())

        # since directory already exists it will abort
        with self.assertRaises(vd.VersionedDirException):
            vd._create_git_repo('snakebuild_git_test_bare', tmp_data_dir())

        # clean up
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))

        # create temporary directory which should not be existing
        os.makedirs(barename)
        with self.assertRaises(vd.VersionedDirException):
            vd._create_git_repo('snakebuild_git_test_bare', tmp_data_dir())
        if os.path.isdir(barename):
            shutil.rmtree(barename)

        # clean up
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))

        # test with not existing git repos location
        with self.assertRaises(vd.VersionedDirException):
            vd._create_git_repo('snakebuild', barename)

        os.makedirs(barename)
        os.chmod(barename, stat.S_IRUSR)

        # test with not writeable repository directory
        with self.assertRaises(vd.VersionedDirException):
            vd._create_git_repo('snakebuild', barename)

        os.chmod(barename, stat.S_IRUSR | stat.S_IWUSR)
        shutil.rmtree(barename)

    def test_clone_git_repos(self):
        ''' The the _clone_git_repo function '''
        barename = os.path.join(tmp_data_dir(), 'snakebuild_git_test_bare')
        clonename1 = os.path.join(tmp_data_dir(), 'snakebuild_git_test_clone1')
        clonename2 = os.path.join(tmp_data_dir(), 'snakebuild_git_test_clone2')

        if os.path.isdir(barename):
            shutil.rmtree(barename)
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))
        if os.path.isdir(clonename1):
            shutil.rmtree(clonename1)
        if os.path.isdir(clonename2):
            shutil.rmtree(clonename2)
        if os.path.isdir('{0}.git'.format(clonename2)):
            shutil.rmtree('{0}.git'.format(clonename2))

        vd._create_git_repo('snakebuild_git_test_bare', tmp_data_dir())
        vd._clone_git_repo('snakebuild_git_test_bare', clonename1,
                tmp_data_dir())

        # try to clone a git repos which does not exist.
        with self.assertRaises(vd.VersionedDirException):
            vd._clone_git_repo('snakebuild_git_test', 'test', tmp_data_dir())

        # try to create a clone again, directory already exists
        os.makedirs(clonename2)
        with self.assertRaises(vd.VersionedDirException):
            vd._clone_git_repo('snakebuild_git_test_bare', clonename1,
                    tmp_data_dir())
        with self.assertRaises(vd.VersionedDirException):
            vd._clone_git_repo('snakebuild_git_test_bare', clonename2,
                    tmp_data_dir())
        shutil.rmtree(clonename2)

        # try to clone an existing directory which isn't a git repos
        if os.path.isdir(clonename1):
            shutil.rmtree(clonename1)
        os.makedirs('{0}.git'.format(clonename2))
        with self.assertRaises(vd.VersionedDirException):
            vd._clone_git_repo(clonename2, clonename1, tmp_data_dir())
        shutil.rmtree('{0}.git'.format(clonename2))

    def test_create_new_repos(self):
        ''' Create several new repositories to test the creat_new_repo fuction.
        '''
        barename = os.path.join(tmp_data_dir(), 'snakebuild_git_test_bare')
        if os.path.isdir(barename):
            shutil.rmtree(barename)
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))

        rconf = vd.ReposConfig(vd.ReposConfig.GIT, tmp_data_dir())
        vd.create_new_repo('snakebuild_git_test_bare', rconf)

        # clean up
        if os.path.isdir(barename):
            shutil.rmtree(barename)
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))

        # change manually since we can't create such a type
        rconf.repo_type = vd.ReposConfig.UNKNOWN
        with self.assertRaises(vd.VersionedDirException):
            vd.create_new_repo('snakebuild_git_test_bare', rconf)

    def test_clone_repos(self):
        ''' Clone a repository to test the clone_repo fuction.
        '''
        barename = os.path.join(tmp_data_dir(), 'snakebuild_git_test_bare')
        clonename = os.path.join(tmp_data_dir(), 'snakebuild_git_test_clone1')
        if os.path.isdir(barename):
            shutil.rmtree(barename)
        if os.path.isdir('{0}.git'.format(barename)):
            shutil.rmtree('{0}.git'.format(barename))
        if os.path.isdir(clonename):
            shutil.rmtree(clonename)

        rconf = vd.ReposConfig(vd.ReposConfig.GIT, tmp_data_dir())
        vd.create_new_repo('snakebuild_git_test_bare', rconf)

        vd.clone_repo('snakebuild_git_test_bare',
                'snakebuild_git_test_clone1', rconf)

        # clean up
        if os.path.isdir(clonename):
            shutil.rmtree(clonename)
        # change manually since we can't create such a type
        rconf.repo_type = vd.ReposConfig.UNKNOWN
        with self.assertRaises(vd.VersionedDirException):
            vd.clone_repo('snakebuild_git_test_bare',
                    'snakebuild_git_test_clone1', rconf)


def _create_clone(origin, clonedir, bare=False):
    ''' Create a clone from an existing repository. Remove the existing
        directroy if the target directory already exists.
    '''
    if os.path.isdir(clonedir):
        shutil.rmtree(clonedir)

    os.makedirs(clonedir)

    if bare:
        subprocess.check_call(['git', 'clone', '--bare', origin, clonedir])
    else:
        subprocess.check_call(['git', 'clone', origin, clonedir])


def _init_git_repo(path):
    ''' Initialize a git repository and populate it with some data to test it.

        @param path: The path to the empty directory to init the git repos
    '''
    prevdir = os.getcwd()
    os.chdir(path)

    subprocess.check_call(['git', 'init'])
    _add_git_file('one', '1')
    _add_git_file('two', '2')
    _add_tag('v1.0', 'first tag')
    _create_branch('v1.x')
    _add_git_file('three', '3')
    _add_tag('v1.1', 'branch tag')
    _add_git_file('threehalf', '3.5')
    _checkout_branch('master')
    _add_git_file('four', '4')
    _add_tag('v2.0', 'add 2.0er tag')

    os.chdir(prevdir)


def _create_branch(name):
    ''' Create a new branch

        @param name: the name of the branch
    '''
    subprocess.check_call(['git', 'checkout', '-b', name])


def _checkout_branch(name):
    ''' checkout a given branch

        @param name: the name of the branch to get
    '''
    subprocess.check_call(['git', 'checkout', name])


def _add_tag(tagname, tagcomment):
    ''' tag the current state.

        @param tagname: The name of the tag
        @param tagcomment: The comment to use for the tag
    '''
    subprocess.check_call(['git', 'tag', '-a', tagname,
            '-m {0}'.format(tagcomment)])


def _add_git_file(filename, content):
    ''' Add a new file to the git repository and add the given content.
        @param filename: The name of the file to add
        @param content: The content of the file
    '''
    newfile = open(filename, 'w')
    newfile.write(content)
    newfile.close()

    subprocess.check_call(['git', 'add', filename])
    subprocess.check_call(['git', 'commit',
        '-m added file {0}'.format(filename)])
