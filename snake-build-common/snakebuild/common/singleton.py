# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>


class Singleton(type):
    ''' This metaclass makes out of an ordinary class a Singleton. Just add
        __metaclass__ = singleton.Singleton before __init__.
    '''
    def __init__(self, *args):
        type.__init__(self, *args)
        self._instances = {}

    def __call__(self, *args):
        if not args in self._instances:
            self._instances[args] = type.__call__(self, *args)
        return self._instances[args]
