# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

from snakebuild import singleton


class Config(object):
    ''' This class allows parsing config files with the json format and
        accessing the parameters.
    '''
    __metaclass__ = singleton.Singleton

    def __init__(self):
        self.ConfigDescription = {}
        self.ApplicationName = ""
