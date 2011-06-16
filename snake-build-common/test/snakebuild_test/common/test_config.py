# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest

from snakebuild.common import Config
from snakebuild.common.config import ConfigValueException


class TestConfig(unittest.TestCase):
    ''' The unit test for the snake build common Config class. '''
    def setUp(self):
        pass

    def test_init_config(self):
        ''' Initialize the config object with default values. '''
        config = Config()
        with self.assertRaises(ConfigValueException):
            config.init_default_config('data/test_config.txt')
