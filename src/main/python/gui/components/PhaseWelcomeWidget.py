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

from lib.AppConfig import app_conf_get

class PhaseWelcomeWidget(QWidget):
    """Phase Welcome widget GUI"""

    def __init__(self, image_cache, i18n, log, cb_next_phase):
        """Initializes the widget

        :param image_cache: The image cache
        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseWelcomeWidget')

        self.image_cache = image_cache
        self.i18n = i18n
        self.log = log
        self.cb_next_phase = cb_next_phase

        self.components = []

        self.is_enabled = False

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWidget GUI')

        font_label_header = QFont()
        font_label_header.setBold(True)
        font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        font_label_info = QFont()
        font_label_info.setBold(False)
        font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        line_css = 'background-color: #c0c0c0;'

        # Components

        label_header = QLabel(self.i18n.translate('GUI.PHASE.WELCOME.HEADER'))
        label_header.setFont(font_label_header)
        label_header.setAlignment(Qt.AlignCenter)

        line_1 = QWidget()
        line_1.setFixedHeight(1)
        line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_1.setStyleSheet(line_css)

        line_2 = QWidget()
        line_2.setFixedHeight(1)
        line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_2.setStyleSheet(line_css)

        label_welcome_text = QLabel(self.i18n.translate('GUI.PHASE.WELCOME.TEXT'))
        label_welcome_text.setFont(font_label_info)
        label_welcome_text.setAlignment(Qt.AlignLeft)

        label_spacer = QLabel('')

        button_start = QPushButton(self.i18n.translate('GUI.PHASE.WELCOME.START'))
        button_start.clicked[bool].connect(self._start)
        self.components.append(button_start)

        # Layout

        grid = QGridLayout()
        grid.setSpacing(20)

        # grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        grid.addWidget(line_1, curr_gridid, 0, 1, 4)
        grid.addWidget(label_header, curr_gridid, 4, 1, 2)
        grid.addWidget(line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        grid.addWidget(label_welcome_text, curr_gridid, 0, 3, 10)

        curr_gridid += 3
        grid.addWidget(label_spacer, curr_gridid, 0, 3, 10)

        curr_gridid += 3
        grid.addWidget(button_start, curr_gridid, 0, 1, 10)

        self.setLayout(grid)
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

    def _start(self):
        """Starts"""
        logging.debug('Starting')
        if self.cb_next_phase:
            self.cb_next_phase()
