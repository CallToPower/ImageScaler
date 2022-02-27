#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Main window"""

import logging
import platform

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction

from i18n.Translations import translate
from gui.components.MainWidget import MainWidget
from gui.components.AboutDialog import AboutDialog


class MainWindow(QMainWindow):
    """Main window GUI"""

    def __init__(selfyodata):
        """Initializes the main window"""
        super().__init__()

        logging.debug('Initializing MainWindow')

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWindow GUI')

        self._init_menu()

        self.setWindowTitle(translate('GUI.MAIN.WINDOW.TITLE'))
        self.statusbar = self.statusBar()

        self.mainwidget = MainWidget(log=self.show_message)
        self.mainwidget.init_ui()
        self.setCentralWidget(self.mainwidget)

        self.resize(800, 500)

        self._center()
        self._init()

    def _show_about_dialog(self):
        """Displays the about dialog"""
        logging.debug('Displaying AboutDialog')
        about = AboutDialog()
        about.init_ui()
        about.exec_()

    def _quit_application(self):
        """Quits the application"""
        logging.info('Quitting')
        QCoreApplication.exit(0)

    def _init_menu(self):
        """Initializes the menu bar"""
        logging.debug('Initializing the menu bar')

        if platform.uname().system.startswith('Darw'):
            logging.debug('Platform is Mac OS')
            self.menu_bar = QMenuBar()
        else:
            logging.debug('Platform is not Mac OS')
            self.menu_bar = self.menuBar()

        menu_application = self.menu_bar.addMenu(
            translate('GUI.MAIN.MENU.APPNAME'))

        action_about = QAction(translate('GUI.MAIN.MENU.ITEM.ABOUT'), self)
        action_about.setShortcut('Ctrl+A')
        action_about.triggered.connect(self._show_about_dialog)

        action_quit = QAction(translate('GUI.MAIN.MENU.ITEM.QUIT'), self)
        action_quit.setShortcut('Ctrl+Q')
        action_quit.triggered.connect(self._quit_application)

        menu_application.addAction(action_about)
        menu_application.addAction(action_quit)

    def _init(self):
        """Initializes the window"""
        logging.debug('Initializing MainWindow defaults')
        self.show_message(translate('GUI.MAIN.LOG.WELCOME_MESSAGE'))

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.geometry().width()) / 2,
                  (screen.height() - self.geometry().height()) / 2)
