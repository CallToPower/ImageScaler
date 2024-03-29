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
from pathlib import Path

_app_config = {
    'author': 'Denis Meyer',
    'version': '2.2.0',
    'build': '2023-09-23-1',
    'copyright': '© 2019-2023 Denis Meyer',
    'conf.folder': 'ImageScaler',
    'conf.name': 'conf.json',
    'language.main': 'en',
    'window.width': 800,
    'window.height': 600,
    'about.logo.scaled.width': 280,
    'about.logo.scaled.height': 80,
    'label.header.font.size': 14,
    'label.header.small.font.size': 12,
    'label.info.font.size': 10,
    'label.info.small.font.size': 8,
    'logging.log_to_file': False,
    'logging.loglevel': 'INFO',
    'logging.format': '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s',
    'logging.datefmt': '%d-%m-%Y %H:%M:%S',
    'logging.logfile': str(Path.home()) + '/ImageScaler/logs/application-' + time.strftime('%d-%m-%Y-%H-%M-%S') + '.log'
}

def get_loglevel():
    """Returns the log level

    :return: The log level
    """
    _loglvl = app_conf_get('logging.loglevel')
    _lvl = logging.INFO
    if _loglvl == 'DEBUG':
        _lvl = logging.DEBUG
    elif _loglvl == 'ERROR':
        _lvl = logging.DEBUG

    return _lvl

def get_public_values():
    """Returns a dict with public values to write to a config file"""
    vals = ['window.width',
            'window.height',
            'label.header.font.size',
            'label.header.small.font.size',
            'label.info.font.size',
            'label.info.small.font.size',
            'language.main',
            'logging.log_to_file',
            'logging.loglevel'
            ]
    _dict = {}
    for val in vals:
        _dict[val] = app_conf_get(val)

    return _dict

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
        logging.error('Returning default for key "%s": "%s"', key, exception)
        return default
