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
''' The unit test for the Config object '''

import unittest
import json
import os.path

from snakebuild.common import Config, AppDirs
from snakebuild.common.config import ConfigValueException


class TestConfig(unittest.TestCase):
    ''' The unit test for the snake build common Config class. '''
    def setUp(self):
        AppDirs().init('snakebuild_test')
        self.config_dir = os.path.join(os.path.dirname(__file__), '..', '..',
                'data')
        data = {"application_name": 'snakebuild_test',
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
        dfd = open(os.path.join(self.config_dir, 'test_data.txt'), 'w')
        dfd.write(json.dumps(data))

    def test_init_config(self):
        ''' Initialize the config object with default values and check values.
        '''
        config = Config()
        with self.assertRaises(ConfigValueException):
            config.init_default_config(os.path.join(self.config_dir,
                    'test_config.txt'))
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        self.assertTrue(config.application_name == 'snakebuild_test')

        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', 'Start')
        self._check_value(config, 'client', 'second', 'Altairians', unicode,
                'Stop', 'Stop')
        self._check_value(config, 'client', 'third', 'Amoeboid Zingatularians',
                int, 12, 12)
        self._check_value(config, 'client', 'forth', 'Bartledanians', float,
                12.2, 12.2)
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool, True,
                True)

        self._check_value(config, 'server', 'first', 'Betelgeusians', str,
                'End', 'End')
        self._check_value(config, 'server', 'second', 'Blagulon Kappans',
                unicode, 'Accelerate', 'Accelerate')
        self._check_value(config, 'server', 'third', 'Dentrassis', int, -12,
                -12)
        self._check_value(config, 'server', 'forth', 'Dolphins', float, 3.3333,
                3.3333)
        self._check_value(config, 'server', 'fifth',
                "G'Gugvunnts and Vl'hurgs", bool, False, False)

    def test_save_default_config(self):
        ''' Test the save functionality of the config module '''
        config = Config()
#        config.init_default_config(os.path.join(self.config_dir,
#                'test_data.txt'))

        config.save(os.path.join(self.config_dir, 'test_default_output.txt'))
        config.save(os.path.join(self.config_dir,
                'test_default_output_verbose.txt'), True)
        config.set('client', 'first', 42)
        config.set('client', 'second', 42)
        config.set('server', 'first', 42)
        config.set('server', 'second', 42)
        config.save(os.path.join(self.config_dir, 'test_save_output.txt'))
        config.save(os.path.join(self.config_dir,
                'test_save_output_verbose.txt'), True)

    def test_set_config(self):
        ''' Test seting and getting values from the config object '''
        config = Config()

        # tests without default config loaded
        config.set('client', 'first', 12)
        value = config.get_s('client', 'first')
        self.assertTrue(type(value) == str)
        # this is a string since we don't now anything about it
        self.assertTrue(value == '12')

        config.set('client', 'third', -16)
        value = config.get_s('client', 'third')
        self.assertTrue(type(value) == str)
        # this is a string since we don't now anything about it
        self.assertTrue(value == '-16')

        # and now with default config loaded
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        # check previous set values if the previous value remains.
        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', "12")
        self._check_value(config, 'client', 'third',
                'Amoeboid Zingatularians', int, 12, -16)

        # now do some test for all kind of types
        config.set('client', 'first', 112)
        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', "112")
        config.set('client', 'second', 12.45)
        self._check_value(config, 'client', 'second', 'Altairians', unicode,
                'Stop', '12.45')
        config.set('client', 'third', -166)
        self._check_value(config, 'client', 'third',
                'Amoeboid Zingatularians', int, 12, -166)
        config.set('client', 'forth', 11)
        self._check_value(config, 'client', 'forth', 'Bartledanians', float,
                12.2, 11.0)
        config.set('client', 'fifth', False)
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool,
                True, False)

        config.set('server', 'first', True)
        self._check_value(config, 'server', 'first', 'Betelgeusians', str,
                'End', 'True')
        config.set('server', 'second', "Arther Dent")
        self._check_value(config, 'server', 'second', 'Blagulon Kappans',
                unicode, 'Accelerate', 'Arther Dent')
        config.set('server', 'third', 42)
        self._check_value(config, 'server', 'third', 'Dentrassis', int, -12,
                42)
        config.set('server', 'forth', 42.43)
        self._check_value(config, 'server', 'forth', 'Dolphins', float,
                3.3333, 42.43)
        config.set('server', 'fifth', True)
        self._check_value(config, 'server', 'fifth',
                "G'Gugvunnts and Vl'hurgs", bool, False, True)

    def _check_value(self, config, section, key, edesc, etype, edefault,
            evalue):
        ''' Check if the given config value has the expected values.
            @param config: The config object to check
            @param section: The section to check
            @param key: The key to check
            @param edesc: Expected Description
            @param etype: Expected type
            @param edefault: Expected default value
            @param evalue: Expected value
        '''
        value = config.get_s(section, key)
        self.assertTrue(type(value) == etype)
        self.assertTrue(value == evalue)
        desc, ctype, default = config.get_description(section, key)
        self.assertTrue(default == edefault)
        self.assertTrue(desc == edesc)
        self.assertTrue(ctype == etype)
