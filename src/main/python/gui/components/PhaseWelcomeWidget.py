#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Phase Welcome widget"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QPushButton

from gui.enums.Language import Language

from lib.AppConfig import app_conf_get


class PhaseWelcomeWidget(QWidget):
    """Phase Welcome widget GUI"""

    def __init__(self, i18n, log, cb_next_phase, cb_change_language, image_cache):
        """Initializes the widget

        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_next_phase: Next phase callback
        :param cb_change_language: Change language callback
        :param image_cache: The image cache
        """
        super().__init__()

        logging.debug('Initializing PhaseWelcomeWidget')

        self.i18n = i18n
        self.log = log
        self.cb_next_phase = cb_next_phase
        self.cb_change_language = cb_change_language
        self.image_cache = image_cache

        self.components = []

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWidget GUI')

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        self.font_label_info = QFont()
        self.font_label_info.setBold(False)
        self.font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        self.line_css = 'background-color: #c0c0c0;'

        # Components

        self.label_header = QLabel(self.i18n.translate('GUI.PHASE.WELCOME.HEADER'))
        self.label_header.setFont(self.font_label_header)
        self.label_header.setAlignment(Qt.AlignCenter)

        self.line_1 = QWidget()
        self.line_1.setFixedHeight(1)
        self.line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_1.setStyleSheet(self.line_css)

        self.line_2 = QWidget()
        self.line_2.setFixedHeight(1)
        self.line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_2.setStyleSheet(self.line_css)

        self.label_welcome_text = QLabel(self.i18n.translate('GUI.PHASE.WELCOME.TEXT'))
        self.label_welcome_text.setFont(self.font_label_info)
        self.label_welcome_text.setAlignment(Qt.AlignLeft)

        self.label_spacer = QLabel('')

        self.button_lang_en = QPushButton(self.i18n.translate('GUI.PHASE.WELCOME.LANG.EN'))
        self.button_lang_en.clicked[bool].connect(self._change_lang_en)
        flag_en = self.image_cache.get_or_load_icon('img.flag.en', 'en.png', 'flags')
        if flag_en is not None:
            self.button_lang_en.setIcon(flag_en)
        self.components.append(self.button_lang_en)

        self.button_lang_de = QPushButton(self.i18n.translate('GUI.PHASE.WELCOME.LANG.DE'))
        self.button_lang_de.clicked[bool].connect(self._change_lang_de)
        flag_de = self.image_cache.get_or_load_icon('img.flag.de', 'de.png', 'flags')
        if flag_de is not None:
            self.button_lang_de.setIcon(flag_de)
        self.components.append(self.button_lang_de)

        self.button_start = QPushButton(self.i18n.translate('GUI.PHASE.WELCOME.START'))
        self.button_start.clicked[bool].connect(self._start)
        self.components.append(self.button_start)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        self.grid.addWidget(self.line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_header, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.label_welcome_text, curr_gridid, 0, 3, 10)

        curr_gridid += 3
        self.grid.addWidget(self.label_spacer, curr_gridid, 0, 3, 10)

        curr_gridid += 3
        if self.i18n.current_language == Language.EN:
            self.grid.addWidget(self.button_lang_de, curr_gridid, 7, 1, 3)
        else:
            self.grid.addWidget(self.button_lang_en, curr_gridid, 7, 1, 3)

        curr_gridid += 1
        self.grid.addWidget(self.button_start, curr_gridid, 0, 1, 10)

        self.setLayout(self.grid)
        self._reset_enabled()

    def reset(self):
        """Resets the widget"""
        logging.debug('Resetting widget')

        self._reset_enabled()

    def _reset_enabled(self):
        """Resets all component to initial state"""
        logging.debug('Resetting components to enabled state')

        self._enable()

    def _disable(self):
        """Resets all component to disabled state"""
        logging.debug('Disabling components')

        self.is_enabled = False
        for comp in self.components:
            comp.setEnabled(False)

    def _enable(self):
        """Resets all component to enabled state"""
        logging.debug('Enabling components')

        for comp in self.components:
            comp.setEnabled(True)
        self.is_enabled = True

    def _change_lang_en(self):
        """Changes language to en"""
        if self.cb_change_language:
            self.cb_change_language(Language.EN)

    def _change_lang_de(self):
        """Changes language to de"""
        if self.cb_change_language:
            self.cb_change_language(Language.DE)

    def _start(self):
        """Starts"""
        logging.debug('Starting')
        if self.cb_next_phase:
            self.cb_next_phase()
