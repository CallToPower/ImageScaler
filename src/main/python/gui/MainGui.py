#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""GUI"""

import logging
import sys

from PyQt5 import QtWidgets

from i18n.I18n import I18n
from lib.ImageCache import ImageCache
from gui.components.MainWindow import MainWindow

from lib.AppConfig import app_conf_get

class GUI():
    """Main GUI"""

    def __init__(self, basedir):
        """Initializes the GUI
        
        :param basedir: The base directory"""
        logging.debug('Initializing MainGUI')
        self.basedir = basedir

        self.image_cache = ImageCache(self.basedir)
        self.i18n = I18n(self.basedir, lang=app_conf_get('language.main'))

    def run(self):
        """Initializes and shows the GUI"""
        logging.debug('Initializing AppContext GUI')

        app = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow(i18n=self.i18n, image_cache=self.image_cache)
        self.main_window.init_ui()
        self.main_window.show()

        app.exec()

        sys.exit(0)
