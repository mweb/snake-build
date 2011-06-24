# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' A Singleton meta class to get a singleton out of your object the easy way.
'''


class Singleton(type):
    ''' This metaclass makes out of an ordinary class a Singleton. Just add
        __metaclass__ = singleton.Singleton before __init__.
    '''
    def __init__(mcs, *args):
        type.__init__(mcs, *args)
        mcs._instances = {}

    def __call__(mcs, *args):
        if not args in mcs._instances:
            mcs._instances[args] = type.__call__(mcs, *args)
        return mcs._instances[args]
