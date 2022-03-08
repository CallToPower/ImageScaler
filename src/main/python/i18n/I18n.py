#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""The I18n"""

import logging

from gui.enums.Language import Language

_translations_en = {
    'SCALED_IMAGE_SUFFIX': '-scaled',
    'PDF.NAME': 'AllImages',
    'GUI.ABOUT.LABEL.AUTHOR': 'Author',
    'GUI.ABOUT.LABEL.COPYRIGHT': 'Copyright',
    'GUI.ABOUT.LABEL.VERSION': 'Version',
    'GUI.ABOUT.LABEL.BUILD': 'Build',
    'GUI.ABOUT.TITLE': 'About ImageScaler',
    'GUI.MAIN.LOG.PHASE.WELCOME': 'Welcome!',
    'GUI.MAIN.LOG.PHASE.INPUT': 'Step 1/3: Select images',
    'GUI.MAIN.LOG.PHASE.OUTPUT': 'Schritt 2/3: Conversion settings',
    'GUI.MAIN.LOG.PHASE.CONVERSION': 'Schritt 3/3: Conversion',
    'GUI.MAIN.LOG.PHASE.DONE': 'Done!',
    'GUI.MAIN.WIDGET.REMOVE': 'Remove',
    'GUI.MAIN.MENU.APPNAME': 'ImageScaler',
    'GUI.MAIN.MENU.ITEM.ABOUT': 'About',
    'GUI.MAIN.MENU.ITEM.QUIT': 'Quit',
    'GUI.MAIN.WINDOW.TITLE': 'ImageScaler',
    'GUI.PHASE.WELCOME.HEADER': 'ImageScaler',
    'GUI.PHASE.WELCOME.TEXT': 'With this app you can scale images and save them in a single PDF file.\n\nThere are three steps:\n\t1.  Select images\n\t2.  Change conversion settings\n\t3.  Convert images\n\nClick "Start" to start with step 1.',
    'GUI.PHASE.WELCOME.START': 'Start',
    'GUI.PHASE.WELCOME.LANG.EN': 'English',
    'GUI.PHASE.WELCOME.LANG.DE': 'Deutsch',
    'GUI.PHASE.INPUT.HEADER': 'Step 1/3: Select images',
    'GUI.PHASE.INPUT.SELECT_IMAGES': 'Select images',
    'GUI.PHASE.INPUT.SELECTED_IMAGES': 'Selected images',
    'GUI.PHASE.INPUT.LOG.SELECT_IMAGES': 'Please select one or more images',
    'GUI.PHASE.INPUT.LOG.SELECT_IMAGES_SUCCESS': '{} images selected',
    'GUI.PHASE.INPUT.LOG.SELECT_IMAGES_CANCEL': 'Cancelled image selection',
    'GUI.PHASE.INPUT.DIALOG.SELECT': 'Select image files',
    'GUI.PHASE.INPUT.NEXT_PHASE': 'Go to Step 2',
    'GUI.PHASE.INPUT.ERROR.NO_IMAGES_SELECTED': 'No images selected',
    'GUI.PHASE.INPUT.ERROR.NEXT_PHASE': 'The next step cannot be started:',
    'GUI.PHASE.INPUT.ERROR.ERROR': 'Error',
    'GUI.PHASE.OUTPUT.LABEL.HEADER': 'Step 2/3: Conversion settings',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE': 'Image size',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_WIDTH': 'px (width)',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_TIMES': '        x',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_HEIGHT': 'px (height)',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_INFO': 'Dynamic scaling is active:  Either width or height can be left blank.',
    'GUI.PHASE.OUTPUT.LABEL.OUTPUT_DIR': 'Output directory',
    'GUI.PHASE.OUTPUT.BUTTON.SELECT_OUTPUT_DIR': 'Select',
    'GUI.PHASE.OUTPUT.LABEL.PDF': 'PDF',
    'GUI.PHASE.OUTPUT.CHECKBOX.CHECKBOX_CREATE_PDF': 'Create PDF file including all images',
    'GUI.PHASE.OUTPUT.NEXT_PHASE': 'Go to step 3',
    'GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR': 'Please select an output directory',
    'GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_SUCCESS': 'Selected "{}" as output directory',
    'GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_CANCEL': 'Cancelled output directory selection',
    'GUI.PHASE.OUTPUT.ERROR.IMAGE_SIZE': 'No valid image size',
    'GUI.PHASE.OUTPUT.ERROR.NO_OUTPUT_DIR_SELECTED': 'No output directory selected',
    'GUI.PHASE.OUTPUT.ERROR.NEXT_PHASE': 'The next step cannot be started:',
    'GUI.PHASE.OUTPUT.ERROR.ERROR': 'Error',
    'GUI.PHASE.CONVERSION.LABEL.HEADER': 'Step 3/3: Conversion',
    'GUI.PHASE.CONVERSION.BUTTON.PROCESS': 'Conversion started',
    'GUI.PHASE.CONVERSION.LABEL.IMAGES': 'Images',
    'GUI.PHASE.CONVERSION.LABEL.IMAGES.TEXT': 'Number of images to be converted: {}',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE': 'Image size',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_WIDTH': 'Width: {} px',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_HEIGHT': 'Height: {} px',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_INFO': 'Dynamic scaling is active if either width or height is not set.',
    'GUI.PHASE.CONVERSION.LABEL.OUTPUT_DIR': 'Output directory',
    'GUI.PHASE.CONVERSION.LABEL.PDF': 'PDF',
    'GUI.PHASE.CONVERSION.LABEL.PDF.TEXT': 'A PDF file including all images will be created.',
    'GUI.PHASE.CONVERSION.LABEL.NO_PDF.TEXT': 'A PDF file including all images will not be created.',
    'GUI.PHASE.CONVERSION.ERROR.IMAGE_SIZE': 'No valid image size',
    'GUI.PHASE.CONVERSION.ERROR.NO_OUTPUT_DIR_SELECTED': 'No output directory selected',
    'GUI.PHASE.CONVERSION.ERROR.NO_IMAGES_SELECTED': 'No images selected',
    'GUI.PHASE.CONVERSION.ERROR.START_PROCESSING': 'The conversion cannot be started:',
    'GUI.PHASE.CONVERSION.ERROR.ERROR': 'Error',
    'GUI.PHASE.CONVERSION.LOG.START_PROCESSING': 'Starting conversion',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.SINGULAR.PDF': '{}/{} image successfully converted, PDF file created',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.PLURAL.PDF': '{}/{} images successfully converted, PDF file created',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.SINGULAR.NO_PDF': '{}/{} image successfully converted',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.PLURAL.NO_PDF': '{}/{} images successfully converted',
    'GUI.PHASE.CONVERSION.LOG.ERROR_PROCESSING': 'Image conversion failed',
    'GUI.PHASE.DONE.HEADER': 'Done!',
    'GUI.PHASE.DONE.TEXT.SINGULAR': '{}/{} image has been successfully converted.',
    'GUI.PHASE.DONE.TEXT.PLURAL': '{}/{} images have been successfully converted.',
    'GUI.PHASE.DONE.TEXT.PDF': 'A PDF file including all images has been created.',
    'GUI.PHASE.DONE.TEXT.NO_PDF': 'A PDF file including all images has not been created.',
    'GUI.PHASE.DONE.NEXT_PHASE': 'Done'
}

_translations_de = {
    'SCALED_IMAGE_SUFFIX': '-skaliert',
    'PDF.NAME': 'AlleBilder',
    'GUI.ABOUT.LABEL.AUTHOR': 'Autor',
    'GUI.ABOUT.LABEL.COPYRIGHT': 'Copyright',
    'GUI.ABOUT.LABEL.VERSION': 'Version',
    'GUI.ABOUT.LABEL.BUILD': 'Build',
    'GUI.ABOUT.TITLE': 'Über ImageScaler',
    'GUI.MAIN.LOG.PHASE.WELCOME': 'Willkommen!',
    'GUI.MAIN.LOG.PHASE.INPUT': 'Schritt 1/3: Bilder auswählen',
    'GUI.MAIN.LOG.PHASE.OUTPUT': 'Schritt 2/3: Konvertierungs-Einstellungen',
    'GUI.MAIN.LOG.PHASE.CONVERSION': 'Schritt 3/3: Konvertierung',
    'GUI.MAIN.LOG.PHASE.DONE': 'Fertig!',
    'GUI.MAIN.WIDGET.REMOVE': 'Entfernen',
    'GUI.MAIN.MENU.APPNAME': 'ImageScaler',
    'GUI.MAIN.MENU.ITEM.ABOUT': 'Über',
    'GUI.MAIN.MENU.ITEM.QUIT': 'Beenden',
    'GUI.MAIN.WINDOW.TITLE': 'ImageScaler',
    'GUI.PHASE.WELCOME.HEADER': 'ImageScaler',
    'GUI.PHASE.WELCOME.TEXT': 'Mit diesem Programm können Bilder skaliert und in einer PDF-Datei zusammengefasst werden.\n\nHierfür werden drei Schritte durchlaufen:\n\t1.  Bilder auswählen\n\t2.  Konvertierungs-Einstellungen vornehmen\n\t3.  Konvertierung der Bilder\n\nKlicke "Starten",  um mit Schritt 1 zu beginnen.',
    'GUI.PHASE.WELCOME.START': 'Starten',
    'GUI.PHASE.WELCOME.LANG.EN': 'English',
    'GUI.PHASE.WELCOME.LANG.DE': 'Deutsch',
    'GUI.PHASE.INPUT.HEADER': 'Schritt 1/3: Bilder auswählen',
    'GUI.PHASE.INPUT.SELECT_IMAGES': 'Bilder auswählen',
    'GUI.PHASE.INPUT.SELECTED_IMAGES': 'Ausgewählte Bilder',
    'GUI.PHASE.INPUT.LOG.SELECT_IMAGES': 'Bitte wähle ein oder mehrere Bilder aus',
    'GUI.PHASE.INPUT.LOG.SELECT_IMAGES_SUCCESS': '{} Bilder ausgewählt',
    'GUI.PHASE.INPUT.LOG.SELECT_IMAGES_CANCEL': 'Bildauswahl abgebrochen',
    'GUI.PHASE.INPUT.DIALOG.SELECT': 'Wähle Bilddateien aus',
    'GUI.PHASE.INPUT.NEXT_PHASE': 'Weiter zu Schritt 2',
    'GUI.PHASE.INPUT.ERROR.NO_IMAGES_SELECTED': 'Keine Bilder ausgewählt',
    'GUI.PHASE.INPUT.ERROR.NEXT_PHASE': 'Der nächste Schritt kann nicht gestartet werden:',
    'GUI.PHASE.INPUT.ERROR.ERROR': 'Fehler',
    'GUI.PHASE.OUTPUT.LABEL.HEADER': 'Schritt 2/3: Konvertierungs-Einstellungen',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE': 'Bildgröße',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_WIDTH': 'px (Breite)',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_TIMES': '        x',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_HEIGHT': 'px (Höhe)',
    'GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_INFO': 'Dynamische Skalierung ist aktiv:  Entweder Breite oder Höhe können leer gelassen werden.',
    'GUI.PHASE.OUTPUT.LABEL.OUTPUT_DIR': 'Ausgabeverzeichnis',
    'GUI.PHASE.OUTPUT.BUTTON.SELECT_OUTPUT_DIR': 'Auswählen',
    'GUI.PHASE.OUTPUT.LABEL.PDF': 'PDF',
    'GUI.PHASE.OUTPUT.CHECKBOX.CHECKBOX_CREATE_PDF': 'PDF-Datei mit allen Bildern erstellen',
    'GUI.PHASE.OUTPUT.NEXT_PHASE': 'Weiter zu Schritt 3',
    'GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR': 'Bitte wähle ein Ausgabeverzeichnis aus',
    'GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_SUCCESS': '"{}" als Ausgabeverzeichnis ausgewählt',
    'GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_CANCEL': 'Ausgabeverzeichniswahl abgebrochen',
    'GUI.PHASE.OUTPUT.ERROR.IMAGE_SIZE': 'Keine valide Bildgröße',
    'GUI.PHASE.OUTPUT.ERROR.NO_OUTPUT_DIR_SELECTED': 'Kein Ausgabeverzeichnis ausgewählt',
    'GUI.PHASE.OUTPUT.ERROR.NEXT_PHASE': 'Der nächste Schritt kann nicht gestartet werden:',
    'GUI.PHASE.OUTPUT.ERROR.ERROR': 'Fehler',
    'GUI.PHASE.CONVERSION.LABEL.HEADER': 'Schritt 3/3: Konvertierung',
    'GUI.PHASE.CONVERSION.BUTTON.PROCESS': 'Konvertierung starten',
    'GUI.PHASE.CONVERSION.LABEL.IMAGES': 'Bilder',
    'GUI.PHASE.CONVERSION.LABEL.IMAGES.TEXT': 'Anzahl zu verarbeitender Bilder: {}',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE': 'Bildgröße',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_WIDTH': 'Breite: {} px',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_HEIGHT': 'Höhe: {} px',
    'GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_INFO': 'Dynamische Skalierung ist aktiv,  falls entweder Breite oder Höhe nicht gesetzt ist.',
    'GUI.PHASE.CONVERSION.LABEL.OUTPUT_DIR': 'Ausgabeverzeichnis',
    'GUI.PHASE.CONVERSION.LABEL.PDF': 'PDF',
    'GUI.PHASE.CONVERSION.LABEL.PDF.TEXT': 'Es wird eine PDF-Datei mit allen vorhandenen Bildern erstellt.',
    'GUI.PHASE.CONVERSION.LABEL.NO_PDF.TEXT': 'Es wird keine PDF-Datei mit allen vorhandenen Bildern erstellt.',
    'GUI.PHASE.CONVERSION.ERROR.IMAGE_SIZE': 'Keine valide Bildgröße',
    'GUI.PHASE.CONVERSION.ERROR.NO_OUTPUT_DIR_SELECTED': 'Kein Ausgabeverzeichnis ausgewählt',
    'GUI.PHASE.CONVERSION.ERROR.NO_IMAGES_SELECTED': 'Keine Bilder ausgewählt',
    'GUI.PHASE.CONVERSION.ERROR.START_PROCESSING': 'Die Konvertierung kann nicht gestartet werden:',
    'GUI.PHASE.CONVERSION.ERROR.ERROR': 'Fehler',
    'GUI.PHASE.CONVERSION.LOG.START_PROCESSING': 'Starte Verarbeitung',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.SINGULAR.PDF': '{}/{} Bild erfolgreich verarbeitet, PDF-Datei erstellt',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.PLURAL.PDF': '{}/{} Bilder erfolgreich verarbeitet, PDF-Datei erstellt',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.SINGULAR.NO_PDF': '{}/{} Bild erfolgreich verarbeitet',
    'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.PLURAL.NO_PDF': '{}/{} Bilder erfolgreich verarbeitet',
    'GUI.PHASE.CONVERSION.LOG.ERROR_PROCESSING': 'Bildverarbeitung fehlgeschlagen',
    'GUI.PHASE.DONE.HEADER': 'Fertig!',
    'GUI.PHASE.DONE.TEXT.SINGULAR': '{}/{} Bild wurde erfolgreich verarbeitet.',
    'GUI.PHASE.DONE.TEXT.PLURAL': '{}/{} Bilder wurden erfolgreich verarbeitet.',
    'GUI.PHASE.DONE.TEXT.PDF': 'Es wurde eine PDF-Datei mit allen vorhandenen Bildern erstellt.',
    'GUI.PHASE.DONE.TEXT.NO_PDF': 'Es wurde keine PDF-Datei mit allen vorhandenen Bildern erstellt.',
    'GUI.PHASE.DONE.NEXT_PHASE': 'Fertig'
}

class I18n():
    """I18n"""

    def __init__(self, lang=Language.EN):
        """Initializing Translations

        :param lang: Default language
        """
        self.current_language = lang
        self._translations = None

        self._set_lang()

    def _set_lang(self):
        """Sets the language"""
        logging.debug('Setting language to {}'.format(self.current_language))
        if self.current_language == Language.DE:
            self._translations = _translations_de
        else:
            self._translations = _translations_en

    def change_language(self, lang):
        """Changes the language
        
        :param lang: The language
        """
        logging.info('Changing language to {}'.format(lang))
        if lang == Language.DE:
            self.current_language = Language.DE
        else:
            self.current_language = Language.EN

        self._set_lang()

    def translate(self, key, default=''):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key to be translated
        :param default: The default if no value could be found for the key
        """
        try:
            return self._translations[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default
