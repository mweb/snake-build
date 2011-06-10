# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

def Client(object):
    ''' This class is simple wrapper class for communication with a server. 
        The message send and receive implmented within this class is a simple
        protocoll where the first byte sent defines the type 
