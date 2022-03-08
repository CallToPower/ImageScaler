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

from i18n.I18n import I18n
from gui.enums.Language import Language
from gui.components.PhaseWelcomeWidget import PhaseWelcomeWidget
from gui.components.PhaseInputWidget import PhaseInputWidget
from gui.components.PhaseOutputWidget import PhaseOutputWidget
from gui.components.PhaseConversionWidget import PhaseConversionWidget
from gui.components.PhaseDoneWidget import PhaseDoneWidget
from gui.components.AboutDialog import AboutDialog
from gui.enums.GUIState import GUIState

from lib.AppConfig import app_conf_get


class MainWindow(QMainWindow):
    """Main window GUI"""

    def __init__(self, image_cache):
        """Initializes the main window

        :param image_cache: The image cache
        """
        super().__init__()

        logging.debug('Initializing MainWindow')

        self.image_cache = image_cache

        self.i18n = I18n(Language.DE)
        self.state = None

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWindow GUI')

        if self._is_in_state(GUIState.INIT_UI):
            logging.warn('Already initializing')
            return

        self._set_state(GUIState.INIT_UI)

        self._init_menu()

        self.setWindowTitle(self.i18n.translate('GUI.MAIN.WINDOW.TITLE'))
        self.statusbar = self.statusBar()

        self.images = []
        self.config = {}
        self.nr_converted_images = 0
        self.nr_all_images = 0

        self._init_phases()

        self.next_phase()

        self.resize(app_conf_get('window.width', 800), app_conf_get('window.height', 500))

        self._center()

    def _show_about_dialog(self):
        """Displays the about dialog"""
        logging.debug('Displaying AboutDialog')
        about = AboutDialog(i18n=self.i18n, image_cache=self.image_cache)
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

        menu_application = self.menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.APPNAME'))

        action_about = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.ABOUT'), self)
        action_about.setShortcut('Ctrl+A')
        action_about.triggered.connect(self._show_about_dialog)

        action_quit = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.QUIT'), self)
        action_quit.setShortcut('Ctrl+Q')
        action_quit.triggered.connect(self._quit_application)

        menu_application.addAction(action_about)
        menu_application.addAction(action_quit)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.geometry().width()) / 2,
                  (screen.height() - self.geometry().height()) / 2)

    def _set_state(self, state):
        """Sets the state

        :param state: The state
        """
        logging.debug('Setting phase: {}'.format(state.name))
        self.state = state

    def _is_in_state(self, state):
        """Checks whether is in a given state

        :param state: The state to check
        """
        return self.state == state

    def _change_language(self, lang):
        """Changes the language

        :param lang: The language
        """
        logging.info('Changing language to {}'.format(lang))
        self.i18n.change_language(lang)

        self._reset_phases()
        self._init_phases()
        self.next_phase()

    def _phase_welcome(self):
        """Phase welcome init"""
        if self._is_in_state(GUIState.PHASE_WELCOME):
            logging.warn('Already in phase {}'.format(self.state.name))
            return
        self._set_state(GUIState.PHASE_WELCOME)
        self.show_message(self.i18n.translate('GUI.MAIN.LOG.PHASE.WELCOME'))

        self.phase_welcome_widget.init_ui()
        self.setCentralWidget(self.phase_welcome_widget)

    def _phase_input(self):
        """Phase input init"""
        if self._is_in_state(GUIState.PHASE_INPUT):
            logging.warn('Already in phase {}'.format(self.state.name))
            return
        self._set_state(GUIState.PHASE_INPUT)
        self.show_message(self.i18n.translate('GUI.MAIN.LOG.PHASE.INPUT'))

        self.phase_input_widget.init_ui()
        self.setCentralWidget(self.phase_input_widget)

    def _phase_output(self):
        """Phase _phase_output init"""
        if self._is_in_state(GUIState.PHASE_OUTPUT):
            logging.warn('Already in phase {}'.format(self.state.name))
            return
        self._set_state(GUIState.PHASE_OUTPUT)
        self.show_message(self.i18n.translate('GUI.MAIN.LOG.PHASE.OUTPUT'))

        self.images = self.phase_input_widget.get_selected_images()
        self.phase_output_widget.init_ui()
        self.setCentralWidget(self.phase_output_widget)

    def _phase_conversion(self):
        """Phase conversion init"""
        if self._is_in_state(GUIState.PHASE_CONVERSION):
            logging.warn('Already in phase {}'.format(self.state.name))
            return
        self._set_state(GUIState.PHASE_CONVERSION)
        self.show_message(self.i18n.translate('GUI.MAIN.LOG.PHASE.CONVERSION'))

        self.config = self.phase_output_widget.get_config()
        self.phase_conversion_widget.set_config(self.images, self.config)
        self.phase_conversion_widget.init_ui()
        self.setCentralWidget(self.phase_conversion_widget)

    def _phase_done(self):
        """Phase done init"""
        if self._is_in_state(GUIState.PHASE_DONE):
            logging.warn('Already in phase {}'.format(self.state.name))
            return
        self._set_state(GUIState.PHASE_DONE)
        self.show_message(self.i18n.translate('GUI.MAIN.LOG.PHASE.DONE'))

        self.nr_converted_images = self.phase_conversion_widget.get_nr_converted_images()
        self.nr_all_images = self.phase_conversion_widget.get_nr_all_images()
        self.config['CREATE_PDF'] = self.phase_conversion_widget.isPdfWritten()
        self.phase_done_widget.set_config(
            self.nr_converted_images,
            self.nr_all_images,
            self.config['CREATE_PDF'])
        self.phase_done_widget.init_ui()
        self.setCentralWidget(self.phase_done_widget)

    def _reset_phases(self):
        """Resets all phases"""
        logging.info('Resetting all phases')

        self._set_state(GUIState.INIT_UI)

        self.setCentralWidget(None)
        self.phase_welcome_widget = None
        self.phase_input_widget = None
        self.phase_output_widget = None
        self.phase_conversion_widget = None
        self.phase_done_widget = None

        self.images = []
        self.config = {}
        self.nr_converted_images = 0
        self.nr_all_images = 0

        self._init_phases()

    def _init_phases(self):
        """Initializes all phases"""
        logging.info('Initializing all phases')

        self.phase_welcome_widget = PhaseWelcomeWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        cb_change_language=self._change_language,
                                        i18n=self.i18n,
                                        image_cache=self.image_cache)
        self.phase_input_widget = PhaseInputWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_output_widget = PhaseOutputWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_conversion_widget = PhaseConversionWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_done_widget = PhaseDoneWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)

    def next_phase(self):
        """Goes to the next phase"""
        logging.info('Current phase: {}'.format(self.state.name))
        if self.state == GUIState.INIT_UI:
            self._phase_welcome()
        elif self.state == GUIState.PHASE_WELCOME:
            self._phase_input()
        elif self.state == GUIState.PHASE_INPUT:
            self._phase_output()
        elif self.state == GUIState.PHASE_OUTPUT:
            self._phase_conversion()
        elif self.state == GUIState.PHASE_CONVERSION:
            self._phase_done()
        elif self.state == GUIState.PHASE_DONE:
            self._reset_phases()
            self._phase_welcome()
        else:
            logging.warn('No next phase defined')

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
