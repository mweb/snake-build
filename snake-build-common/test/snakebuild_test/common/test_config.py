# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

import unittest
import json

from snakebuild.common import Config
from snakebuild.common.config import ConfigValueException


class TestConfig(unittest.TestCase):
    ''' The unit test for the snake build common Config class. '''
    def setUp(self):
        data = {"application_name": 'snakebuile_test',
                "Client": {
                    "first": {"default": "Start", "type": "str",
                        "description": "Aldebarans"},
                    "second": {"default": "Stop", "type": "unicode",
                        "description": "Altairians"},
                    "third": {"default": 12, "type": "int",
                        "description": "Amoeboid Zingatularians"},
                    "forth": {"default": 12.2, "type": "float",
                        "description": "Bartledanians"},
                    "fifth": {"default": True, "type": "bool",
                        "description": "Belcerebons"}},
                "Server": {
                    "first": {"default": "End", "type": "str",
                        "description": "Betelgeusians"},
                    "second": {"default": "Accelerate", "type": "unicode",
                        "description": "Blagulon Kappans"},
                    "third": {"default": -12, "type": "int",
                        "description": "Dentrassis"},
                    "forth": {"default": 3.3333, "type": "float",
                        "description": "Dolphins"},
                    "fifth": {"default": False, "type": "bool",
                        "description": "G'Gugvunnts and Vl'hurgs"}}}
        f = open('data/test_data.txt', 'w')
        f.write(json.dumps(data))

    def test_init_config(self):
        ''' Initialize the config object with default values. '''
        config = Config()
        with self.assertRaises(ConfigValueException):
            config.init_default_config('data/test_config.txt')
        config.init_default_config('data/test_data.txt')

