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
''' The unit test for the application directories functions and object '''

import unittest
import sys
import os
import tempfile

from snakebuild.common.appdirs import user_data_dir, shared_data_dir, \
        shared_config_dir, tmp_data_dir, log_dir
from snakebuild.common import platform


class TestAppdirs(unittest.TestCase):
    ''' The unit test for the snake build appdirs functions. '''
    def setUp(self):
        # fake that the application is installed to get the different file 
        # outputs
        platform.__installed__ = True

    def test_user_data_dir(self):
        ''' Test if the user data directory is correct. '''
        path = user_data_dir('snake-build', 'snakes')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.expanduser('~/.config/snake-build'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(os.path.expanduser(
                    '~/Library/Application Support'), 'snake-build'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)

        # now with version
        path = user_data_dir('snake-build', 'snakes', '1.2')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.expanduser(
                    '~/.config/snake-build/1.2'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(os.path.expanduser(
                    '~/Library/Application Support'), 'snake-build', '1.2'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)


    def test_shared_data_dir(self):
        ''' Test if the shared data directory is correct. '''
        path = shared_data_dir('snake-build', 'snakes')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.join('/usr/share/', 'snake-build'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(
                    '/Library/Application Support', 'snake-build'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)

        # now with version
        path = shared_data_dir('snake-build', 'snakes', '2.3')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.join('/usr/share/', 'snake-build',
                    '2.3'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(
                    '/Library/Application Support', 'snake-build', '2.3'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)

    def test_shared_config_dir(self):
        ''' Test if the shared config directory is correct. '''
        path = shared_config_dir('snake-build', 'snakes')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.join('/etc', 'snake-build'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(
                    '/Library/Application Support', 'snake-build'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)

        # now with version
        path = shared_config_dir('snake-build', 'snakes', '1.0')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.join('/etc', 'snake-build', '1.0'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(
                    '/Library/Application Support', 'snake-build', '1.0'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)

    def test_tmp_data_dir(self):
        ''' Test if the temp data directory is correct.
        '''
        path = tmp_data_dir()
        self.assertTrue(path == tempfile.gettempdir())

    def test_log_dir(self):
        ''' Test if the log directory is correct. '''
        path = log_dir('snake-build', 'snakes')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.join('/var/log', 'snake-build'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(os.path.expanduser(
                    '~/Library/Logs'), 'snake-build'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)

        # now with version
        path = log_dir('snake-build', 'snakes', '4.2')
        if sys.platform.startswith("linux"):
            self.assertTrue(path == os.path.join('/var/log', 'snake-build',
                    '4.2'))
        elif sys.platform == 'darwin':
            self.assertTrue(path == os.path.join(os.path.expanduser(
                    '~/Library/Logs'), 'snake-build', '4.2'))
        elif sys.platform.startswith('win'):
            print 'Unit test not yet implemented for windows'
            self.assertTrue(False)
        else:
            print ('Your platform is currently not supported. %s ' %
                    sys.platform)
            self.assertTrue(False)
