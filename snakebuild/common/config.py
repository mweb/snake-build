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
''' This file holds Config class for loading/storing the configuration of the
    Project.
'''

# python imports
import os
import json
import logging
import ConfigParser

# common imports
from snakebuild.i18n import _
from snakebuild.common import output
from snakebuild.common.appdirs import AppDirs

LOG = logging.getLogger('snakebuild.common.config')


class ConfigValueException(BaseException):
    ''' The exception thrown if a problem within the Config object occures. '''


class Config(object, ConfigParser.SafeConfigParser):
    ''' This handles config files. The config files have the following
        structure: (See doc/config.txt)
        [SECTIONNAME]
        param1 = 'test'
        param2 = test
        param3 = 12

        The section name defines the section the following parameters can be
        accessed.
        For storing values that should not be written to the config file the
        section 'hidden' can be used. This section will never be written to
        a config file. But it is possible to have it within the config file.
        This group can be used for storing passwords.
    '''

    def __init__(self):
        ConfigParser.SafeConfigParser.__init__(self)
        self.config_description = {}
        self.application_name = ""

    def init_default_config(self, path):
        ''' Initialize the config object and load the default configuration.
            The path to the config file must be provided. The name of the
            application is read from the config file.
            The config file stores the description and the default values for
            all configurations including the application name.

            @param path: The path to the config config file.
        '''
        if not (os.path.exists(path) and os.path.isfile(path)):
            raise ConfigValueException(_('The given config config file does '
                    'not exist. ({0})').format(path))
        cfl = open(path, 'r')
        data = json.load(cfl)
        for key in data.iterkeys():
            if 'application_name' == key:
                self.application_name = data[key].lower()
                continue
            self._add_section_default(key, data[key])

    def get_description(self, section, key):
        ''' Get the description of a config key. If it does not exist an
            Exception will be thrown.

            @param section: the section where the key is stored.
            @param key:     the key to get the description for.
            @return: A tuple with three elements First
        '''
        if section in self.config_description:
            if key in self.config_description[section]:
                return self.config_description[section][key]
            else:
                if self.has_option(section, key):
                    # return an empty string since it is possible that a
                    # section is not initialized, this happens if a plugin
                    # that has some config values but is not initialized.
                    return "", str, ""
                else:
                    raise ConfigValueException(_('Key ({0}) does not exist '
                            'in section: {1}').format(key, section))
        else:
            if self.has_section(section):
                # return an empty string since it is possible that a section
                # is not initialized, this happens if a plugin that has some
                # config values but is not initialized.
                return "", str, ""
            else:
                raise ConfigValueException(_('Section does not exist '
                        '[{0}]').format(section))

    def load_default(self):
        ''' Load the default config files.
            First the global config file then the user config file.
        '''
        self.load(AppDirs().get_shared_config_file("%s.conf" %
                self.application_name.lower()))
        if os.getuid() > 0:
            config_path = AppDirs().get_user_file('.%s' %
                    self.application_name.lower())
            config_file = os.path.join(config_path, "%s.conf" %
                            self.application_name)
            if os.path.exists(config_file):
                self.load(config_file)

    def load(self, filename):
        ''' Load the given config file.

            @param filename: the filename including the path to load.
        '''
        if not os.path.exists(filename):
            #print 'Could not load config file [%s]' % (filename)
            return
        self.readfp(open(filename))

    def get_s(self, section, key):
        ''' Get the value of a key in the given section. It will automatically
            translate the paramter type if the parameter has a type specified
            with the description.

            @param section: the section where the key can be found.
            @param key: the key the value is stored under.
            @return the value as a string or the specified type.
            @exception: if the type is specified and the value could not be
                    translated to the given type.
        '''
        section = section.lower()
        key = key.lower()
        descr, value_type, default = self.get_description(section, key)
        if value_type == bool:
            return self.getboolean(section, key)

        return value_type(ConfigParser.SafeConfigParser.get(self, section,
                key))

    def set(self, section, key, value):
        ''' Set the value for a key in the given section. It will check the
            type of the value if it is available. If the value is not from
            the given type it will be transformed to the type.
            An exception will be thrown if there is a problem with the
            conversion.

            @param section: the section of the key
            @param key: the key where to store the valu
            @param value: the value to store
            @exception: If there is a problem with the conversation of the
                    value type.
        '''
        value_type = str
        if self.has_option(section, key):
            descr, value_type, default = self.get_description(section, key)

        if value_type != type(value):
            if value_type == bool:
                try:
                    if (value.lower() == 'true' or value.lower() == 't' or
                            int(value) > 0):
                        value = True
                    elif (value.lower() == 'false' or value.lower() == 'f' or
                            int(value) == 0):
                        value = False
                    else:
                        raise ConfigValueException(_('Could not convert '
                                'boolean type: {0}').format(value))
                except:
                    raise ConfigValueException(_('Could not convert %s to '
                            'type boolean').format(value))
            else:
                value = value_type(value)

        if not self.has_section(section):
            self.add_section(section)

        ConfigParser.SafeConfigParser.set(self, section, key, str(value))

    def save(self, filename=None, verbose=False):
        ''' Save the config to the given file or the set default location.

            @param filename: the file to write the config
            @param verbose: If set to true the config file will have all values
                    and all descriptions
        '''
        if filename is None:
            if (not self.has_section(self.application_name) or
                    not self.has_option(self.application_name, 'config_file')):
                if not self.has_section(self.application_name):
                    self.add_section(self.application_name)
                if not self.application_name in self.config_description:
                    self.config_description[self.application_name] = {}
                value = os.path.join(os.path.expanduser('~'),
                        '.%s' % self.application_name, '%s.conf' %
                        self.application_name)
                if not self.has_option(self.application_name, 'config_file'):
                    self.set(self.application_name, 'config_file', value)
                if not ('config_file' in
                        self.config_description[self.application_name]):
                    self.config_description[self.application_name]\
                            ['config_file'] = (_('The config file to '
                                'overwrite on change of the config values. '
                                '[$HOME/.{0}/{0}.conf]').format(
                                    self.application_name), str, value)

            filename = self.get(self.application_name, 'config_file')

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        hidden = None
        if self.has_section('hidden'):
            hidden = self.items('hidden')
            self.remove_section('hidden')

        cfp = open(filename, 'w')
#        self.write(cfp)
        self._write_config(cfp, verbose)

        if hidden is not None:
            for key, value in hidden:
                self.set('hidden', key, value)

    def _write_config(self, filedesc, verbose=False):
        ''' Write the current config to the given filedescriptor which has must
            be opened for writing.
            Only the config values different from the default value are written

            If the verbose switch is turned on the config file generated will
            have all values including the default values shown but they will
            be commented out. In addition the description of each paramters
            is stored before the value.

            @param filedesc: The file to write the config into
            @param verbose: The switch between the minimalistic and the more
                    verbose config file.
        '''
        desc = []
        for section in self.sections():
            if section.lower() == '' or section.lower() == 'hidden':
                continue
            desc.append("")
            desc.append('[%s]' % section)
            for key in self.options(section):
                descr, value_type, default = self.get_description(section, key)
                if verbose:
                    desc.append(output.format_message(descr, "# ", 78))
                    desc.append("# Type: [%s]" % str(value_type))
                    desc.append("# %s=%s" % (key, default))
                if not self.get_s(section, key) == default:
                    desc.append('%s=%s' % (key, self.get_s(section, key)))
                if verbose:
                    desc.append("")

        filedesc.write("%s\n" % ("\n".join(desc[1:])))

    def _add_section_default(self, section, parameters):
        ''' Add the given section with the given paramters to the config. The
            parameters must be a dictionary with all the keys to add. Each key
            must be specified as an other dictionary with the following
            parameters: default, description, type

            @param section: The section to add
            @param parameters: The paramters dictionary
        '''
        section = section.lower()
        if not self.has_section(section):
            self.add_section(section)

        if not section in self.config_description:
            self.config_description[section] = {}

        for key, value in parameters.iteritems():
            key = key.lower()
            if not ('default' in value and 'type' in value and
                    'description' in value):
                raise ConfigValueException(_('For the given key no all '
                        'required values are defined.'))
            if not self.has_option(section, key):
                self.set(section, key, value['default'])
            vtype = _get_type(value['type'])
            self.config_description[section][key] = (value['description'],
                    vtype, value['default'])


def _get_type(stype):
    ''' Get the python type for a given string describtion for a type.

        @param stype: The string representing the type to return
        @return: The python type if available
    '''
    stype = stype.lower()
    if stype == 'str':
        return str
    if stype == 'unicode':
        return unicode
    if stype == 'int':
        return int
    if stype == 'float':
        return float
    if stype == 'bool':
        return bool
    raise ConfigValueException(_('Unsuported type given: {0}').format(stype))
