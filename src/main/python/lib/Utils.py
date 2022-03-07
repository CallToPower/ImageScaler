import os
import logging
from pathlib import Path

from PyQt5.QtGui import QPixmap, QIcon

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
