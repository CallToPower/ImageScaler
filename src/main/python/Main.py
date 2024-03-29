#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Main"""

import os
import logging

from lib.AppConfig import app_conf_get, get_loglevel
from gui.MainGui import GUI

def _initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        _basedir = os.path.dirname(app_conf_get('logging.logfile'))

        if not os.path.exists(_basedir):
            os.makedirs(_basedir)

    _lvl = get_loglevel()

    logging.basicConfig(level=_lvl,
                        format=app_conf_get('logging.format'),
                        datefmt=app_conf_get('logging.datefmt'))

    if app_conf_get('logging.log_to_file'):
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding=None, delay=False)
        handler_file.setLevel(_lvl)
        handler_file.setFormatter(logging.Formatter(fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)

if __name__ == '__main__':
    print(f'Current working directory: {os.getcwd()}')

    _initialize_logger()

    basedir = os.path.dirname(__file__)

    gui = GUI(basedir)
    gui.run()
