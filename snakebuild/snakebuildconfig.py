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

''' THIS IS snakebuild-common CONFIGURATION FILE
    YOU CAN PUT THERE SOME GLOBAL VALUE
    Do not touch unless you know what you're doing.
    you're warned :)
'''

__all__ = [
    'INSTALLED'
    ]

# Where your project will look for your data (for instance, images and ui
# files). By default, this is ../data, relative your trunk layout
__license__ = 'Mathias Weber, 2006-2011'
INSTALLED = False

import gettext
#from gettext import gettext as _
gettext.textdomain('snakebuild')
