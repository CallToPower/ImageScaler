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
import platform

_app_config = {
    'author': 'Denis Meyer',
    'version': '2.3.1',
    'build': '2024-09-01-1',
    'copyright': '© 2019-2024 Denis Meyer',
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

_public_value_fields = [
    'window.width',
    'window.height',
    'language.main',
    'logging.log_to_file',
    'logging.loglevel'
]

def is_macos():
    """Returns whether current os is macos
    
    :return: true if current os is macos, false else
    """
    return platform.system() == 'Darwin'

if is_macos():
    """Sets some attributes if current OS is macOS"""
    _app_config_macos = dict(_app_config)
    _app_config_macos['label.header.font.size'] = 18
    _app_config_macos['label.header.small.font.size'] = 16
    _app_config_macos['label.info.font.size'] = 14
    _app_config_macos['label.info.small.font.size'] = 12

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
    return {val: app_conf_get(val) for val in _public_value_fields}

def app_conf_set(key, value):
    """Sets the value for the given key

    :param key: The key
    :param value: The value
    """
    if is_macos():
        _app_config_macos[key] = value
    else:
        _app_config[key] = value

def app_conf_get(key, default=''):
    """Returns the value for the given key or - if not found - a default value

    :param key: The key
    :param default: The default if no value could be found for the key
    """
    try:
        return _app_config_macos[key] if is_macos() else _app_config[key]
    except KeyError as exception:
        logging.error('Returning default for key "%s": "%s"', key, exception)
        return default
