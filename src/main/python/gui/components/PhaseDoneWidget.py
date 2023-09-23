#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Phase Done widget"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QPushButton

from lib.AppConfig import app_conf_get

class PhaseDoneWidget(QWidget):
    """Phase Done widget GUI"""

    def __init__(self, image_cache, i18n, log, cb_next_phase):
        """Initializes the widget

        :param image_cache: The image cache
        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseDoneWidget')

        self.image_cache = image_cache
        self.i18n = i18n
        self.log = log
        self.cb_next_phase = cb_next_phase

        self.components = []

        self.nr_images_converted = 0
        self.nr_images_all = 0
        self.pdf_created = True

        self.is_enabled = False

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseDoneWidget GUI')

        font_label_header = QFont()
        font_label_header.setBold(True)
        font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        font_label_info = QFont()
        font_label_info.setBold(False)
        font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        line_css = 'background-color: #c0c0c0;'

        # Components

        label_done_header = QLabel(self.i18n.translate('GUI.PHASE.DONE.HEADER'))
        label_done_header.setFont(font_label_header)
        label_done_header.setAlignment(Qt.AlignLeft)

        line_1 = QWidget()
        line_1.setFixedHeight(1)
        line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_1.setStyleSheet(line_css)

        line_2 = QWidget()
        line_2.setFixedHeight(1)
        line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_2.setStyleSheet(line_css)

        label_done_text = QLabel(self.i18n.translate(f'GUI.PHASE.DONE.TEXT.{"SINGULAR" if self.nr_images_converted == 1 else "PLURAL"}')
                                                     .format(self.nr_images_converted, self.nr_images_all))

        label_done_text_pdf = QLabel(self.i18n.translate('GUI.PHASE.DONE.TEXT.PDF'))

        label_done_text_no_pdf = QLabel(self.i18n.translate('GUI.PHASE.DONE.TEXT.NO_PDF'))

        label_spacer = QLabel('')

        button_finish = QPushButton(self.i18n.translate('GUI.PHASE.DONE.NEXT_PHASE'))
        button_finish.clicked[bool].connect(self._finish)
        self.components.append(button_finish)

        # Layout

        grid = QGridLayout()
        grid.setSpacing(20)

        # grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        grid.addWidget(line_1, curr_gridid, 0, 1, 1)
        grid.addWidget(label_done_header, curr_gridid, 1, 1, 3)
        grid.addWidget(line_2, curr_gridid, 4, 1, 1)

        curr_gridid += 1
        grid.addWidget(label_done_text, curr_gridid, 0, 1, 5)

        curr_gridid += 1
        if self.pdf_created:
            grid.addWidget(label_done_text_pdf, curr_gridid, 0, 1, 5)
        else:
            grid.addWidget(label_done_text_no_pdf, curr_gridid, 0, 1, 5)

        curr_gridid += 1
        grid.addWidget(label_spacer, curr_gridid, 0, 7, 5)

        curr_gridid += 8
        grid.addWidget(button_finish, curr_gridid, 0, 1, 5)

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

    def _finish(self):
        """Finishes"""
        logging.debug('Finshing')
        if self.cb_next_phase:
            self.cb_next_phase()

    def set_config(self, nr_images_converted, nr_images_all, pdf_created):
        """Sets the config

        :param nr_images_converted: Number of converted images
        :param nr_images_all: Number of all images to be converted
        :param pdf_created: Boolean flag whether a PDF file has been created
        """
        self.nr_images_converted = nr_images_converted
        self.nr_images_all = nr_images_all
        self.pdf_created = pdf_created
