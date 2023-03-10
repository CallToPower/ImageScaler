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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QMessageBox

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

    def __init__(self, i18n, image_cache):
        """Initializes the main window

        :param i18n: The i18n
        :param image_cache: The image cache
        """
        super().__init__()

        logging.debug('Initializing MainWindow')

        self.i18n = i18n
        self.image_cache = image_cache

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
        self.pdf_written = False

        self._init_phases()

        self.next_phase()

        self.resize(app_conf_get('window.width', 800), app_conf_get('window.height', 600))

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

        logo = self.image_cache.get_or_load_pixmap('img.logo', 'logo.png')
        if logo is not None:
            self.setWindowIcon(QIcon(logo))

        self.menu_application = self.menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.APPNAME'))

        self.action_about = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.ABOUT'), self)
        self.action_about.setShortcut('Ctrl+A')
        self.action_about.triggered.connect(self._show_about_dialog)

        self.action_quit = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.QUIT'), self)
        self.action_quit.setShortcut('Ctrl+Q')
        self.action_quit.triggered.connect(self._quit_application)

        self.menu_application.addAction(self.action_about)
        self.menu_application.addAction(self.action_quit)

        if len(self.i18n.languages) > 1:
            self.menu_language = self.menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE'))

            for lang in self.i18n.languages:
                action = QAction(lang, self)
                flag = self.image_cache.get_or_load_icon('img.flag.{}'.format(lang), '{}.png'.format(lang), 'flags')
                if flag:
                    action.setIcon(flag)
                action.triggered.connect(self._action_change_language)
                self.menu_language.addAction(action)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.geometry().width()) / 2),
                  int((screen.height() - self.geometry().height()) / 2))

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

    def _action_change_language(self):
        self._change_language(self.sender().text())

    def _change_language(self, lang):
        """Changes the language

        :param lang: The language
        """
        if lang == self.i18n.language_main:
            return

        if not self._is_in_state(GUIState.PHASE_WELCOME):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE.CHANGE.WARN.TEXT'))
            msg_box.setWindowTitle(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE.CHANGE.WARN.TITLE'))
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msg_box_return = msg_box.exec()
        else:
            msg_box_return = QMessageBox.Ok

        if msg_box_return == QMessageBox.Ok:
            self.i18n.change_language(lang)

            self.menu_application.setTitle(self.i18n.translate('GUI.MAIN.MENU.APPNAME'))
            self.action_about.setText(self.i18n.translate('GUI.MAIN.MENU.ITEM.ABOUT'))
            self.action_quit.setText(self.i18n.translate('GUI.MAIN.MENU.ITEM.QUIT'))
            if len(self.i18n.languages) > 1:
                self.menu_language.setTitle(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE'))

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
        self.phase_output_widget.set_images(self.images)
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
        self.pdf_written = self.phase_conversion_widget.isPdfWritten()
        self.phase_done_widget.set_config(
            self.nr_converted_images,
            self.nr_all_images,
            self.pdf_written)
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
        self.pdf_written = False

        self._init_phases()

    def _init_phases(self):
        """Initializes all phases"""
        logging.info('Initializing all phases')

        self.phase_welcome_widget = PhaseWelcomeWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_input_widget = PhaseInputWidget(
                                        log=self.show_message,
                                        cb_cancel=self.cancel,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_output_widget = PhaseOutputWidget(
                                        log=self.show_message,
                                        cb_cancel=self.cancel,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_conversion_widget = PhaseConversionWidget(
                                        log=self.show_message,
                                        cb_cancel=self.cancel,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)
        self.phase_done_widget = PhaseDoneWidget(
                                        log=self.show_message,
                                        cb_next_phase=self.next_phase,
                                        i18n=self.i18n)

    def cancel(self):
        """Cancels and resets"""
        self._reset_phases()
        self._phase_welcome()

    def next_phase(self):
        """Goes to the next phase"""
        logging.debug('Switching from phase: {}'.format(self.state.name))
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
        logging.info('Current phase: {}'.format(self.state.name))

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
