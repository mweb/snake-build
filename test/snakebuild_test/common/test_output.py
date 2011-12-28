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
''' The unit test for the output functions '''

import unittest

from snakebuild.common import output


class TestOutput(unittest.TestCase):
    ''' The unit test for the snake build common output functions. '''
    def setUp(self):
        ''' Setup the test case. '''
        pass

    def test_format_message(self):
        ''' Test the format message method from the output module.
        '''
        # simple one liner with a prefix
        test = "Test"
        value = output.format_message(test, indent="# ", line_length=78)
        self.assertTrue(value == "# Test")

        # simple short text with a starting prefix on each line
        test = "Test to print a longer text"
        value = output.format_message(test, indent="# ", line_length=10)
        self.assertTrue(value == "# Test to\n# print a\n# longer\n# text")

        # simple short text with a tab for indent
        test = "Test to print a longer text"
        value = output.format_message(test, indent="#\t", line_length=13)
        self.assertTrue(value == "#    Test to\n#    print a\n#    longer\n#"
                "    text")

        # simple short text with a tabs in the text
        test = "Test to print a \tlonger text"
        value = output.format_message(test, indent="# ", line_length=10)
        self.assertTrue(value == "# Test to\n# print a\n#     longer\n#"
                " text")

        # simple short text with a a differnt indent for the first line
        test = "Test to print a longer text"
        value = output.format_message(test, indent="# ", line_length=10,
                first_indent="#!/bin/sh ")
        self.assertTrue(value == "#!/bin/sh Test\n# to print\n# a longer\n#"
                " text")

    def test_formatted_output(self):
        ''' Test if the formatted output is working properly (without errors
            wuring call.
        '''
        output.warning("Test warning message")
        output.error("Test error message")
