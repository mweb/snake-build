#!/usr/bin/env python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

############## DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ##################

import os
import sys
import shutil

from distutils.core import setup
from distutils.command.build import build
from distutils.spawn import find_executable, spawn


def find_packages(path='.'):
    ''' Find all python packate to install them.

        @param path: The path to start search for the packages.
    '''
    walker = os.walk(path)
    result = []
    for path, directories, filenames in walker:
        if '__init__.py' in filenames:
            result.append(path)

    return result


def find_data(search_path, install_path='share/snakebuild_common'):
    ''' find all data files and create a list with the install targets.

        @param search_path: The path to search for files
        @param install_path: The default path to install the files

        TODO: add support for other platforms than Linux
    '''
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


def update_version_file(version):
    ''' Set the version within snakebuild/__init__.py to the current installed
        version.

        @param version: The version string to set
    '''
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


def update_installed_flag(installed):
    ''' update the installed flag within the common/platform module 
        @param installed: set the __installed__ flag to this value (boolean)
    '''
    try:
        fin = file('snakebuild/common/platform.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if '__installed__ =' in line:
                line = "__installed__ = %s\n" % (installed)
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print ("ERROR: Can't find snakebuild/common/platform.py")
        sys.exit(1)


class InstallAndUpdateDataDirectory(build):
    def run(self):
        update_installed_flag(True)
        update_version_file(self.distribution.get_version())
        self.build_mo()
        build.run(self)
        update_installed_flag(False)

    def build_mo(self):
        if not find_executable('msgfmt'):
            self.warn("msgfmt executable could not be found -> no "
                    'translations will be built')

        podir = 'i18n'
        if not os.path.isdir(podir):
            self.warn('could not find %s directory' % podir)
            return

        for po in os.listdir(podir):
            if not po.endswith('.po'):
                continue
            pofile = os.path.join(podir, po)
            modir = os.path.join('locale', po[:-3], 'LC_MESSAGES')
            mofile = os.path.join(modir, 'snakebuild.mo')
            mobuildfile = os.path.join('snakebuild', mofile)
            cmd = ['msgfmt' , '-v', '-o', mobuildfile, pofile, '-c']

            self.mkpath(os.path.join('snakebuild', modir))
            self.make_file([pofile], mobuildfile, spawn, (cmd,))
        if os.path.isdir('locale'):
            shutil.rmtree('locale')
        shutil.move(os.path.join('snakebuild', 'locale'), 'locale')


##############################################################################
################### YOU SHOULD MODIFY ONLY WHAT IS BELOW #####################
##############################################################################

setup(
    name='snakebuild',
    version='0.1.0',
    license='GPL v3.0',
    author='Mathias Weber',
    author_email='mathew.weber@gmail.com',
    description='The snake-build build server with all its components',
    long_description='The snake-build build server is a build server which '
            'provides fully versioned config and build instructions.',
    cmdclass={'build': InstallAndUpdateDataDirectory},
    packages=find_packages('snakebuild'),
    scripts=['bin/sb-resourceclient', 'bin/sb-resourceserver'],
    data_files=(find_data('data', 'share/snakebuild') +
            find_data('etc', '/etc') + find_data('locale', 'locale') +
            find_data('doc', 'share/doc/snakebuild')),
    )
