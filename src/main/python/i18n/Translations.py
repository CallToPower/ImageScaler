#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

import logging

"""The translation table"""

_translations_en = {
    'SCALED_IMAGE_SUFFIX': '-scaled',
    'GUI.ABOUT.LABEL.AUTHOR': 'Author',
    'GUI.ABOUT.LABEL.COPYRIGHT': 'Copyright',
    'GUI.ABOUT.LABEL.VERSION': 'Version',
    'GUI.ABOUT.LABEL.BUILD': 'Build',
    'GUI.ABOUT.TITLE': 'About ImageScaler',
    'GUI.MAIN.BUTTON.SELECT_IMAGES': 'Browse for Images',
    'GUI.MAIN.BUTTON.SELECT_OUTPUT_DIR': 'Select',
    'GUI.MAIN.BUTTON.PROCESS': 'Start Processing',
    'GUI.MAIN.ERROR.ERROR': 'Error',
    'GUI.MAIN.ERROR.START_PROCESSING': 'Cannot start processing:',
    'GUI.MAIN.ERROR.IMAGE_SIZE': 'No valid image size',
    'GUI.MAIN.ERROR.NO_OUTPUT_DIR_SELECTED': 'No output directory selected',
    'GUI.MAIN.ERROR.NO_IMAGES_SELECTED': 'No source images selected',
    'GUI.MAIN.LABEL.IMAGE_SIZE': 'Image Size:',
    'GUI.MAIN.LABEL.IMAGE_SIZE_WIDTH': 'px (Width)',
    'GUI.MAIN.LABEL.IMAGE_SIZE_TIMES': '     x',
    'GUI.MAIN.LABEL.IMAGE_SIZE_HEIGHT': 'px (Height)',
    'GUI.MAIN.LABEL.IMAGE_SIZE_INFO': 'Dynamic Scaling is active. It is possible to leave width or height blank.',
    'GUI.MAIN.LABEL.OUTPUT_DIR': 'Directory:',
    'GUI.MAIN.LABEL.PDF': 'PDF:',
    'GUI.MAIN.CHECKBOX.CHECKBOX_CREATE_PDF': 'Create PDF file containing all images',
    'GUI.MAIN.LABEL.INPUT': 'Input',
    'GUI.MAIN.LABEL.SETTINGS': 'Output',
    'GUI.MAIN.LABEL.PROCESS': 'Processing',
    'GUI.MAIN.LABEL.SELECTED_IMAGES': 'Selected Images:',
    'GUI.MAIN.LOG.SELECT_IMAGES': 'Please select one or more images',
    'GUI.MAIN.LOG.SELECT_IMAGES_SUCCESS': 'Selected {} images',
    'GUI.MAIN.LOG.SELECT_IMAGES_CANCEL': 'Cancelled selecting images',
    'GUI.MAIN.LOG.SELECT_OUTPUT_DIR': 'Please select an output directory',
    'GUI.MAIN.LOG.SELECT_OUTPUT_DIR_SUCCESS': 'Selected output directory is "{}"',
    'GUI.MAIN.LOG.SELECT_OUTPUT_DIR_CANCEL': 'Cancelled selecting output directory',
    'GUI.MAIN.LOG.START_PROCESSING': 'Starting processing',
    'GUI.MAIN.LOG.DONE_PROCESSING': 'Successfully processed {}/{} images',
    'GUI.MAIN.LOG.ERROR_PROCESSING': 'Failed to process images',
    'GUI.MAIN.LOG.WELCOME_MESSAGE': 'Welcome!',
    'GUI.MAIN.DIALOG.SELECT': 'Select Files',
    'GUI.MAIN.WIDGET.REMOVE': 'Remove',
    'GUI.MAIN.MENU.APPNAME': 'ImageScaler',
    'GUI.MAIN.MENU.ITEM.ABOUT': 'About',
    'GUI.MAIN.MENU.ITEM.QUIT': 'Quit',
    'GUI.MAIN.WINDOW.TITLE': 'ImageScaler'
}

_translations_de = {
    'SCALED_IMAGE_SUFFIX': '-skaliert',
    'GUI.ABOUT.LABEL.AUTHOR': 'Autor',
    'GUI.ABOUT.LABEL.COPYRIGHT': 'Copyright',
    'GUI.ABOUT.LABEL.VERSION': 'Version',
    'GUI.ABOUT.LABEL.BUILD': 'Build',
    'GUI.ABOUT.TITLE': 'Über ImageScaler',
    'GUI.MAIN.BUTTON.SELECT_IMAGES': 'Bilder auswählen',
    'GUI.MAIN.BUTTON.SELECT_OUTPUT_DIR': 'Auswählen',
    'GUI.MAIN.BUTTON.PROCESS': 'Konvertierung starten',
    'GUI.MAIN.ERROR.ERROR': 'Fehler',
    'GUI.MAIN.ERROR.START_PROCESSING': 'Konvertierung kann nicht gestartet werden:',
    'GUI.MAIN.ERROR.IMAGE_SIZE': 'Keine valide Bildgröße',
    'GUI.MAIN.ERROR.NO_OUTPUT_DIR_SELECTED': 'Kein Ausgabeverzeichnis ausgewählt',
    'GUI.MAIN.ERROR.NO_IMAGES_SELECTED': 'Keine Bildquellen ausgewählt',
    'GUI.MAIN.LABEL.IMAGE_SIZE': 'Bildgröße:',
    'GUI.MAIN.LABEL.IMAGE_SIZE_WIDTH': 'px (Breite)',
    'GUI.MAIN.LABEL.IMAGE_SIZE_TIMES': '     x',
    'GUI.MAIN.LABEL.IMAGE_SIZE_HEIGHT': 'px (Höhe)',
    'GUI.MAIN.LABEL.IMAGE_SIZE_INFO': 'Dynamische Skalierung ist aktiv. Breite oder Höhe können leer gelassen werden.',
    'GUI.MAIN.LABEL.OUTPUT_DIR': 'Verzeichnis:',
    'GUI.MAIN.LABEL.PDF': 'PDF:',
    'GUI.MAIN.CHECKBOX.CHECKBOX_CREATE_PDF': 'PDF-Datei mit allen Bildern erstellen',
    'GUI.MAIN.LABEL.INPUT': 'Eingabe',
    'GUI.MAIN.LABEL.SETTINGS': 'Ausgabe',
    'GUI.MAIN.LABEL.PROCESS': 'Verarbeite',
    'GUI.MAIN.LABEL.SELECTED_IMAGES': 'Ausgewählte Bilder:',
    'GUI.MAIN.LOG.SELECT_IMAGES': 'Bitte wähle ein oder mehrere Bilder aus',
    'GUI.MAIN.LOG.SELECT_IMAGES_SUCCESS': '{} Bilder ausgewählt',
    'GUI.MAIN.LOG.SELECT_IMAGES_CANCEL': 'Bildauswahl abgebrochen',
    'GUI.MAIN.LOG.SELECT_OUTPUT_DIR': 'Bitte wähle ein Ausgabeverzeichnis aus',
    'GUI.MAIN.LOG.SELECT_OUTPUT_DIR_SUCCESS': '"{}" als Ausgabeverzeichnis ausgewählt',
    'GUI.MAIN.LOG.SELECT_OUTPUT_DIR_CANCEL': 'Ausgabeverzeichniswahl abgebrochen',
    'GUI.MAIN.LOG.START_PROCESSING': 'Starte Verarbeitung',
    'GUI.MAIN.LOG.DONE_PROCESSING': '{}/{} Bilder erfolgreich verarbeitet',
    'GUI.MAIN.LOG.ERROR_PROCESSING': 'Bildverarbeitung fehlgeschlagen',
    'GUI.MAIN.LOG.WELCOME_MESSAGE': 'Willkommen!',
    'GUI.MAIN.DIALOG.SELECT': 'Wähle Bilddateien aus',
    'GUI.MAIN.WIDGET.REMOVE': 'Entfernen',
    'GUI.MAIN.MENU.APPNAME': 'ImageScaler',
    'GUI.MAIN.MENU.ITEM.ABOUT': 'Über',
    'GUI.MAIN.MENU.ITEM.QUIT': 'Beenden',
    'GUI.MAIN.WINDOW.TITLE': 'ImageScaler'
}

# TODO
_translations = _translations_de


def translate(key, default=''):
    """Returns the value for the given key or - if not found - a default value

    :param key: The key to be translated
    :param default: The default if no value could be found for the key
    """
    try:
        return _translations[key]
    except KeyError as exception:
        logging.error(
            'Returning default for key "{}": "{}"'.format(key, exception))
        return default
