#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""AppConfig"""

import logging
import time
import tempfile
import os


_app_config = {
    'author': 'Denis Meyer',
    'version': '2.0.0',
    'build': '2022-03-08-1',
    'copyright': '© 2019-2022 Denis Meyer',
    'window.width': 800,
    'window.height': 500,
    'about.logo.scaled.width': 280,
    'about.logo.scaled.height': 80,
    'label.header.font.size': 20,
    'label.header.small.font.size': 18,
    'label.info.font.size': 16,
    'label.info.small.font.size': 12,
    'logging.log_to_file': False,
    'logging.loglevel': logging.DEBUG,
    'logging.format': '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s',
    'logging.datefmt': '%d-%m-%Y %H:%M:%S',
    'logging.logfile': os.path.join(os.getcwd(), 'logs', 'py-imgscaler.application-{}.log'.format(time.strftime('%d-%m-%Y-%H-%M-%S')))
}


def app_conf_set(key, value):
    """Sets the value for the given key

    :param key: The key
    :param value: The value
    """
    _app_config[key] = value


def app_conf_get(key, default=''):
    """Returns the value for the given key or - if not found - a default value

    :param key: The key
    :param default: The default if no value could be found for the key
    """
    try:
        return _app_config[key]
    except KeyError as exception:
        logging.error('Returning default for key "{}": "{}"'.format(key, exception))
        return default
