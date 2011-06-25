# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' The command line parser of the sb-resourceserver application. '''

from optparse import OptionParser


def parse_command_line():
    ''' Read the command line and parse it. All command line arguments are
        specified within this method.
    '''
    usage = 'usage: %prog [OPTIONS]\n'

    parser = OptionParser(usage)
    parser.add_option('-f', '--configfile', dest='configfile', metavar='FILE',
        help='The configfile to load. This will be the last file to be '
        'loaded and it will be overwritten for storing a new '
        'configuration.', default=None)
    parser.add_option('--foreground', dest='foreground', action='store_true',
            help="Run the server in foreground instead of background", 
            default=False)
    parser.add_option('-v', '--version', dest='version', action='store_true',
            help='Ask for the version.', default=False)

    (options, args) = parser.parse_args()

    return options, args
