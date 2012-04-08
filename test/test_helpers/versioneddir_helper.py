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
''' The functions in this file provide some helper functions for the tests to
    handle versioned directories (create, remove,...)
'''

import shutil
import os

from snakebuild.common.appdirs import tmp_data_dir
from snakebuild.common.versioneddir import ReposConfig, create_new_repo, \
        clone_repo, get_versioned_directory


def create_versioned_dir_all(name):
    ''' Create a new versioned directory with the given name. Two new
        directories will be created within the tmp directory. One for the
        bare repository and one for the checked out repos.

        @param: The name of the repository to use.
        @return: A tuple with the versioneddir object ready to use and the
                bare repos path
    '''
    base_dir = os.path.join(tmp_data_dir(), 'snakebuild_{0}_bare'.format(name))
    repos_dir = os.path.join(tmp_data_dir(), 'snakebuild_{0}'.format(name))

    if os.path.isdir(base_dir):
        shutil.rmtree(base_dir)
    if os.path.isdir(repos_dir):
        shutil.rmtree(repos_dir)
    os.makedirs(base_dir)
    repos_config = ReposConfig(ReposConfig.GIT, base_dir)
    create_new_repo(name, repos_config)
    clone_repo(name, repos_dir, repos_config)
    repo = get_versioned_directory(repos_dir)

    return repo, base_dir

def create_versioned_dir(name):
    ''' Create a new versioned directory with the given name. Two new
        directories will be created within the tmp directory. One for the
        bare repository and one for the checked out repos.

        @param: The name of the repository to use.
        @return: The versioneddir object ready to use.
    '''
    return create_versioned_dir_all(name)[0]
