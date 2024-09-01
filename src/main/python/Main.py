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
from gui.GUI import GUI

def _initialize_logger():
    """Initializes the logger"""
    _log_to_file = app_conf_get('logging.log_to_file')
    _logfile = app_conf_get('logging.logfile')

    if _log_to_file:
        _basedir = os.path.dirname(_logfile)

        if not os.path.exists(_basedir):
            os.makedirs(_basedir)

    _lvl = get_loglevel()
    _fmt = app_conf_get('logging.format')
    _date_fmt = app_conf_get('logging.datefmt')

    logging.basicConfig(level=_lvl, format=_fmt, datefmt=_date_fmt)

    if _log_to_file:
        handler_file = logging.FileHandler(_logfile, mode='w', encoding=None, delay=False)
        handler_file.setLevel(_lvl)
        handler_file.setFormatter(logging.Formatter(fmt=_fmt, datefmt=_date_fmt))
        logging.getLogger().addHandler(handler_file)

if __name__ == '__main__':
    print(f'Current working directory: {os.getcwd()}')

    _initialize_logger()

    basedir = os.path.dirname(__file__)

    print(f'Base directory: {basedir}')

    gui = GUI(basedir)
    gui.run()
