#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2020 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Application Context"""

import logging

from fbs_runtime.application_context import ApplicationContext, cached_property
from PyQt5.QtGui import QPixmap

from lib.AppConfig import app_conf_get, app_conf_set
from gui.components.MainWindow import MainWindow


class AppContext(ApplicationContext):
    """Application Context"""

    def __init__(self):
        """Initializes the GUI"""
        super().__init__()

        logging.debug('Initializing AppContext')

        app_conf_set('img_logo_app', self.img_logo_app)

    @cached_property
    def img_logo_app(self):
        """The application logo"""
        return QPixmap(self.get_resource('logo-app.png'))

    def run(self):
        """Initializes and shows the GUI"""
        logging.debug('Initializing AppContext GUI')

        self.main_window = MainWindow()
        self.main_window.init_ui()
        self.main_window.show()

        return self.app.exec_()
