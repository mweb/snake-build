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
''' The unit test for the Config object '''

import unittest
import tempfile
import os.path
import shutil

from snakebuild.common import filetools


class TestFileTools(unittest.TestCase):
    ''' The unit test for the snake build common filetools.functions. '''

    def setUp(self):
        ''' Setup the test case. Create a tmp directory, that willbe
            removed.
        '''
        self.tmpdir = tempfile.mkdtemp('snakebuildtest')

    def tearDonw(self):
        ''' Clean up the test case (remove the tmp directory).
        '''
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def test_read_full_line(self):
        ''' Test the read full line function. This function is expected to
            read lines with a line ending and return None if there is no
            such line.
        '''
        lines = ['Test line One\n', 'Test line Two\n', 'Test line Three']
        wfile = open(os.path.join(self.tmpdir, 'full.txt'), 'w')
        for line in lines:
            wfile.write(line)
        wfile.flush()

        rfile = open(os.path.join(self.tmpdir, 'full.txt'), 'r')
        self.assertTrue(filetools.read_full_line(rfile) == lines[0])
        self.assertTrue(filetools.read_full_line(rfile) == lines[1])
        self.assertTrue(filetools.read_full_line(rfile) == None)

        wfile.write('\n')
        wfile.flush()
        self.assertTrue(filetools.read_full_line(rfile) ==
                "{0}\n".format(lines[2]))
        self.assertTrue(filetools.read_full_line(rfile) == None)

        wfile.write('Test\n')
        wfile.flush()
        self.assertTrue(filetools.read_full_line(rfile) == 'Test\n')
        self.assertTrue(filetools.read_full_line(rfile) == None)

    def test_tail(self):
        ''' Test the tail function. This function allows getting the last
            few lines of a file. Depending on your configuration.
        '''
        lines = ['Test line One', 'Test line Two', 'Test line Three',
                'Test line Four', 'Test line Five', 'Test line Six']
        wfile = open(os.path.join(self.tmpdir, 'tail.txt'), 'w')
        for line in lines:
            wfile.write("{0}\n".format(line))
        wfile.flush()

        rfile = open(os.path.join(self.tmpdir, 'tail.txt'), 'r')
        read_lines = filetools.tail(rfile, 3)
        self.assertTrue(len(read_lines) == 3)
        self.assertTrue(read_lines[0] == lines[3])
        self.assertTrue(read_lines[1] == lines[4])
        self.assertTrue(read_lines[2] == lines[5])

        wfile.write('Test')
        wfile.flush()
        read_lines = filetools.tail(rfile, 3)
        self.assertTrue(len(read_lines) == 3)
        self.assertTrue(read_lines[0] == lines[4])
        self.assertTrue(read_lines[1] == lines[5])
        self.assertTrue(read_lines[2] == 'Test')

        # test windows file endings
        lines = ['Test line One', 'Test line Two', 'Test line Three',
                'Test line Four', 'Test line Five', 'Test line Six']
        for line in lines:
            wfile.write("{0}\r\n".format(line))
        wfile.flush()
        read_lines = filetools.tail(rfile, 3)
        self.assertTrue(len(read_lines) == 3)
        self.assertTrue(read_lines[0] == lines[3])
        self.assertTrue(read_lines[1] == lines[4])
        self.assertTrue(read_lines[2] == lines[5])

        # now try reading with a buffer size going onto a new line
        read_lines = filetools.tail(rfile, 3, 13)
        self.assertTrue(len(read_lines) == 3)
        self.assertTrue(read_lines[0] == lines[3])
        self.assertTrue(read_lines[1] == lines[4])
        self.assertTrue(read_lines[2] == lines[5])

