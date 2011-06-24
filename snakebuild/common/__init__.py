# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>
''' The common package from the snakebuild provide common classes which might
    be used from all kind other packages.
'''

from snakebuild.common.singleton import Singleton
from config import Config
from logger import create_logger, set_logging_to_config_values
import output
