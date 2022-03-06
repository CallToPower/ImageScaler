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
import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon

from lib.AppConfig import app_conf_get, app_conf_set
from gui.components.MainWindow import MainWindow

class GUI():
    """Main GUI"""

    def __init__(self, basedir):
        """Initializes the GUI
        
        :param basedir: The base directory"""
        logging.debug('Initializing MainGUI')
        self.basedir = basedir


    def img_logo_app(self):
        """The application logo"""
        path = os.path.join(self.basedir, 'resources', 'logo-app.png')
        logging.debug('Getting {}'.format(path))
        return QPixmap(path) if os.path.exists(path) else None


    def img_flag(self, lang):
        """The application logo
        
        :param lang: Language
        """
        path = os.path.join(self.basedir, 'resources', 'flags', '{}.png'.format(lang))
        logging.debug('Getting {}'.format(path))
        return QIcon(path) if os.path.exists(path) else None


    def run(self):
        """Initializes and shows the GUI"""
        logging.debug('Initializing AppContext GUI')

        app = QtWidgets.QApplication(sys.argv)

        app_conf_set('img.logo_app', self.img_logo_app())
        app_conf_set('img.flag.en', self.img_flag('en'))
        app_conf_set('img.flag.de', self.img_flag('de'))

        self.main_window = MainWindow()
        self.main_window.init_ui()
        self.main_window.show()

        app.exec()

        sys.exit(0)
