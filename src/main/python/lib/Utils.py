import os
import json
import logging
from pathlib import Path

from PyQt5.QtGui import QPixmap, QIcon

def load_languages(basedir):
    """Loads the available languages

    :param basedir: The base path
    """
    logging.info('Loading available languages')
    path = os.path.join(basedir, 'resources', 'i18n')
    lang_files = [f[:-len('.json')] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
    logging.info('Available languages: {}'.format(lang_files))
    return lang_files

def load_i18n(basedir, lang):
    """Loads the i18n

    :param basedir: The base path
    :param lang: The language
    """
    file_path = os.path.join(basedir, 'resources', 'i18n', '{}.json'.format(lang))
    logging.info('Trying to load translations from "{}"'.format(file_path))

    translations = {}
    
    if os.path.isfile(file_path):
        logging.info('Translations exist. Loading.')
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                translations = json.load(jsonfile)
        except Exception as ex:
            logging.error('Failed loading from "{}": {}'.format(file_path, ex))
    else:
        logging.info('Translations "{}" do not exist.'.format(file_path))

    return translations

def load_pixmap(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "{}" from directory "{}"'.format(file, file_path))
    try:
        return QPixmap(file_path) if os.path.exists(file_path) else None
    except:
        raise SystemExit('Could not load image "{}"'.format(file_path))

def load_icon(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "{}" from directory "{}"'.format(file, file_path))
    try:
        return QIcon(file_path) if os.path.exists(file_path) else None
    except:
        raise SystemExit('Could not load image "{}"'.format(file_path))
