import os
import json
import logging
from pathlib import Path

from PyQt5.QtGui import QPixmap, QIcon

from lib.AppConfig import app_conf_get, get_loglevel

def update_logging(loglevel, logtofile=False):
    """Updates the logging

    :param loglevel: DEBUG, INFO, ERROR
    :param logtofile: Flag whether to log to file
    """
    logging.info('Setting log level to "%s"', loglevel)
    _lvl = get_loglevel()
    logging.getLogger().setLevel(_lvl)

    if logtofile:
        logging.info('Logging to file')
        basedir = os.path.dirname(app_conf_get('logging.logfile'))
        try:
            if not os.path.exists(basedir):
                os.makedirs(basedir)
        except Exception as ex:
            logging.error('Failed creating a new directory "%s": %s', basedir, ex)
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding='utf-8', delay=False)
        handler_file.setLevel(_lvl)
        handler_file.setFormatter(logging.Formatter(fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)
    else:
        logging.info('Not logging to file')

def _load_conf(file_path):
    """Loads the configuration

    :param file_path: The file path
    :return loaded, config
    """
    config = {}
    loaded = False
    if os.path.isfile(file_path):
        logging.info('Config exists. Loading from "%s"', file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                config = json.load(jsonfile)
                loaded = True
        except Exception as ex:
            logging.error('Failed loading from "%s": %s', file_path, ex)

    return loaded, config

def load_conf_from_home_folder():
    """Loads the configuration from home folder
    
    :return Loadec config
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.folder')
    file = app_conf_get('conf.name')

    file_path = os.path.join(homedir, homefolder, file)
    logging.info('Trying to load configuration from home directory "%s"', file_path)

    return _load_conf(file_path)

def save_conf(config):
    """Saves the configuration to the home directory

    :param config: The config
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.folder')
    file = app_conf_get('conf.name')

    home_dir_path = os.path.join(homedir, homefolder)
    file_path = os.path.join(homedir, homefolder, file)

    logging.info('Writing config to home directory "%s"', file_path)
    try:
        if not os.path.exists(home_dir_path):
            os.makedirs(home_dir_path)
    except Exception as ex:
        logging.error('Failed creating a new directory in home directory "%s": %s', home_dir_path, ex)

    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(config, jsonfile)
    except Exception as ex:
        logging.error('Failed writing to "%s": %s', file_path, ex)

def load_languages(basedir):
    """Loads the available languages

    :param basedir: The base path
    :return: Languages
    """
    logging.info('Loading available languages')
    path = os.path.join(basedir, 'resources', 'i18n')
    lang_files = [f[:-len('.json')] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
    logging.info('Available languages: %s', lang_files)
    return lang_files

def load_i18n(basedir, lang):
    """Loads the i18n

    :param basedir: The base path
    :param lang: The language
    :return: Translations
    """
    file_path = os.path.join(basedir, 'resources', 'i18n', f'{lang}.json')
    logging.info('Trying to load translations from "%s"', file_path)

    translations = {}

    if os.path.isfile(file_path):
        logging.info('Translations exist. Loading.')
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                translations = json.load(jsonfile)
        except Exception as ex:
            logging.error('Failed loading from "%s": %s', file_path, ex)
    else:
        logging.info('Translations "%s" do not exist.', file_path)

    return translations

def load_pixmap(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    :return: Image
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "%s" from directory "%s"', file, file_path)
    try:
        return QPixmap(file_path) if os.path.exists(file_path) else None
    except Exception as ex:
        logging.error('Could not load image "%s"', file_path)
        raise SystemExit(f'Could not load image "{file_path}"') from ex

def load_icon(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    :return: Icon image
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "%s" from directory "%s"', file, file_path)
    try:
        return QIcon(file_path) if os.path.exists(file_path) else None
    except Exception as ex:
        logging.error('Could not load image "%s"', file_path)
        raise SystemExit(f'Could not load image "{file_path}"') from ex
