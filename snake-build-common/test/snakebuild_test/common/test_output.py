# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' The unit test for the Config object '''

import unittest

from snakebuild.common import output


class TestOutput(unittest.TestCase):
    ''' The unit test for the snake build common Config class. '''
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
