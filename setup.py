#!/usr/bin/env python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

############## DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ##################

import os
import sys

from distutils.core import setup
from distutils.command.install import install


def find_packages(path='.'):
    walker = os.walk(path)
    result = []
    for path, directories, filenames in walker:
        if '__init__.py' in filenames:
            result.append(path)

    return result


def find_data(search_path, install_path='share/snakebuild_common'):
    walker = os.walk(search_path, topdown=True)
    result = []
    for path, directories, filenames in walker:
        resultfiles = []
        for name in filenames:
            resultfiles.append(os.path.join(path, name))
        pathname = path[len(search_path):]
        while pathname.startswith('/'):
            pathname = pathname[1:]
        result.append((os.path.join(install_path, pathname), resultfiles))

    return result


def update_data_path(prefixdata, prefixconfig, olddatavalue=None,
        oldconfigvalue=None):

    try:
        fin = file('snakebuild/snakebuildconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ')  # Separate variable from value
            if fields[0] == '__snakebuild_data_directory__':
                # update to prefix, store oldvalue
                if not olddatavalue:
                    olddatavalue = fields[1]
                    line = "%s = '%s'\n" % (fields[0], prefixdata)
                else:  # restore oldvalue
                    line = "%s = %s" % (fields[0], olddatavalue)
            if fields[0] == '__snakebuild_config_directory__':
                # update to prefix, store oldvalue
                if not oldconfigvalue:
                    oldconfigvalue = fields[1]
                    line = "%s = '%s'\n" % (fields[0], prefixconfig)
                else:  # restore oldvalue
                    line = "%s = %s" % (fields[0], oldconfigvalue)

            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print ("ERROR: Can't find snakebuild/snakebuildconfig.py")
        sys.exit(1)
    return olddatavalue, oldconfigvalue


def update_version_file(version):

    try:
        fin = file('snakebuild/__init__.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if '__version__ =' in line:
                line = "__version__ = '%s'\n" % (version)
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print ("ERROR: Can't find snakebuild/__init__.py")
        sys.exit(1)


class InstallAndUpdateDataDirectory(install):
    def run(self):
        previous_values = update_data_path(self.prefix +
            '/share/snakebuild/',
            '/etc/snakebuild')
        update_version_file(self.distribution.get_version())
        install.run(self)
        update_data_path(self.prefix, self.prefix, *previous_values)


##############################################################################
################### YOU SHOULD MODIFY ONLY WHAT IS BELOW #####################
##############################################################################

setup(
    name='snakebuild-common',
    version='0.01.00',
    license='Copyright: (C) 2006-2011 Mathias Weber',
    author='Mathias Weber',
    author_email='mathew.weber@gmail.com',
    description='The common libraries for the snake build build server '
            'components.',
    long_description='The common libraries which are used by all components '
            'of the snake build build server. This includes config and helper '
            'tools.',
    #url='https://launchpad.net/pycsmbuilder',
    cmdclass={'install': InstallAndUpdateDataDirectory},
    packages=find_packages('snakebuild'),
    install_requires=[],
    scripts=[],
    data_files=(find_data('data', 'share/snakebuild') +
            find_data('etc', '/etc')),
    )
