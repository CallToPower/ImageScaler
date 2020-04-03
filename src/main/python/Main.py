#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2020 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Main"""

import os
import logging
import urllib.request
import json

from lib.AppConfig import app_conf_get
from gui.MainGui import GUI


def _initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        basedir = os.path.dirname(app_conf_get('logging.logfile'))

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    logging.basicConfig(level=app_conf_get('logging.loglevel'),
                        format=app_conf_get('logging.format'),
                        datefmt=app_conf_get('logging.datefmt'))

    if app_conf_get('logging.log_to_file'):
        handler_file = logging.FileHandler(
            app_conf_get('logging.logfile'), mode='w', encoding=None, delay=False)
        handler_file.setLevel(app_conf_get('logging.loglevel'))
        handler_file.setFormatter(logging.Formatter(
            fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)


if __name__ == '__main__':
    _initialize_logger()

    gui = GUI()
