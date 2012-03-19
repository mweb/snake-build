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

    def test_git_commands(self):
        ''' Test the internal git command methods.
        '''
        versioned = vd.VersionedGitDir(self.tempgitdir)
        self.assertTrue(versioned._gitr('branch') == 0)


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
