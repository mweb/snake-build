# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' The unit test for the Config object '''

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
        dfd = open('data/test_data.txt', 'w')
        dfd.write(json.dumps(data))

    def test_init_config(self):
        ''' Initialize the config object with default values and check values.
        '''
        config = Config()
        with self.assertRaises(ConfigValueException):
            config.init_default_config('data/test_config.txt')
        config.init_default_config('data/test_data.txt')

        self.assertTrue(config.application_name == 'snakebuile_test')

        self._check_value('client', 'first', 'Aldebarans', str, 'Start',
                'Start')
        self._check_value('client', 'second', 'Altairians', unicode, 'Stop',
                'Stop')
        self._check_value('client', 'third', 'Amoeboid Zingatularians', int,
                12, 12)
        self._check_value('client', 'forth', 'Bartledanians', float, 12.2,
                12.2)
        self._check_value('client', 'fifth', 'Belcerebons', bool, True, True)

        self._check_value('server', 'first', 'Betelgeusians', str, 'End',
                'End')
        self._check_value('server', 'second', 'Blagulon Kappans', unicode,
                'Accelerate', 'Accelerate')
        self._check_value('server', 'third', 'Dentrassis', int, -12, -12)
        self._check_value('server', 'forth', 'Dolphins', float, 3.3333, 3.3333)
        self._check_value('server', 'fifth', "G'Gugvunnts and Vl'hurgs", bool,
                False, False)

    def test_set_config(self):
        ''' Test seting and getting values from the config object '''
        config = Config()
        config.set('client', 'first', 12)
        self._check_value('client', 'first', 'Aldebarans', str, 'Start', "12")
        config.set('client', 'second', 12.45)
        self._check_value('client', 'second', 'Altairians', unicode, 'Stop',
                '12.45')
        config.set('client', 'third', -16)
        self._check_value('client', 'third', 'Amoeboid Zingatularians', int,
                12, -16)
        config.set('client', 'forth', 11)
        self._check_value('client', 'forth', 'Bartledanians', float, 12.2,
                11.0)
        config.set('client', 'fifth', False)
        self._check_value('client', 'fifth', 'Belcerebons', bool, True, False)

        config.set('server', 'first', True)
        self._check_value('server', 'first', 'Betelgeusians', str, 'End',
                'True')
        config.set('server', 'second', "Arther Dent")
        self._check_value('server', 'second', 'Blagulon Kappans', unicode,
                'Accelerate', 'Arther Dent')
        config.set('server', 'third', 42)
        self._check_value('server', 'third', 'Dentrassis', int, -12, 42)
        config.set('server', 'forth', 42.43)
        self._check_value('server', 'forth', 'Dolphins', float, 3.3333, 42.43)
        config.set('server', 'fifth', True)
        self._check_value('server', 'fifth', "G'Gugvunnts and Vl'hurgs", bool,
                False, True)

    def _check_value(self, section, key, edesc, etype, edefault, evalue):
        ''' Check if the given config value has the expected values.
            @param section: The section to check
            @param key: The key to check
            @param edesc: Expected Description
            @param etype: Expected type
            @param edefault: Expected default value
            @param evalue: Expected value
        '''
        value = Config().get_s(section, key)
        self.assertTrue(type(value) == etype)
        self.assertTrue(value == evalue)
        desc, ctype, default = Config().get_description(section, key)
        self.assertTrue(default == edefault)
        self.assertTrue(desc == edesc)
        self.assertTrue(ctype == etype)
