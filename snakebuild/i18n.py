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
''' The snakebuild internationalization handliner '''

import gettext

TRANS = gettext.translation('snakebuild', fallback=True)
_ = TRANS.ugettext

def translate(message):
    ''' Translate a given message. This is used for the shell command
        descriptions, since they are not normal text but comments which we
        need to translate by hand. (And extract as well)
    '''
    if message is None:
        return "None"

    sections = message.split('\n\n')
    translated = []
    for section in sections:
        if section is not None and len(section) > 0:
            translated.append(TRANS.ugettext(section))
        else:
            translated.append('')

    return translated
