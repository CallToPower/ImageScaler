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


class PhaseDoneWidget(QWidget):
    """Phase Done widget GUI"""

    def __init__(self, i18n, log, cb_next_phase):
        """Initializes the widget

        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseDoneWidget')

        self.i18n = i18n
        self.log = log
        self.cb_next_phase = cb_next_phase

        self.components = []

        self.nr_images_converted = 0
        self.nr_images_all = 0
        self.pdf_created = True

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseDoneWidget GUI')

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(20)

        self.font_label_info = QFont()
        self.font_label_info.setBold(False)
        self.font_label_info.setPointSize(16)

        # Components

        self.label_done_header = QLabel(self.i18n.translate('GUI.PHASE.DONE.HEADER'))
        self.label_done_header.setFont(self.font_label_header)
        self.label_done_header.setAlignment(Qt.AlignLeft)

        self.label_done_text = QLabel(self.i18n.translate('GUI.PHASE.DONE.TEXT.{}'.format('SINGULAR' if self.nr_images_converted == 1 else 'PLURAL')).format(self.nr_images_converted, self.nr_images_all))

        self.label_done_text_pdf = QLabel(self.i18n.translate('GUI.PHASE.DONE.TEXT.PDF'))

        self.label_done_text_no_pdf = QLabel(self.i18n.translate('GUI.PHASE.DONE.TEXT.NO_PDF'))

        self.label_spacer = QLabel('')

        self.button_finish = QPushButton(self.i18n.translate('GUI.PHASE.DONE.NEXT_PHASE'))
        self.button_finish.clicked[bool].connect(self._finish)
        self.components.append(self.button_finish)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        self.grid.addWidget(self.label_done_header, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_done_text, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        if self.pdf_created:
            self.grid.addWidget(self.label_done_text_pdf, curr_gridid, 0, 1, 10)
        else:
            self.grid.addWidget(self.label_done_text_no_pdf, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_spacer, curr_gridid, 0, 7, 10)

        curr_gridid += 8
        self.grid.addWidget(self.button_finish, curr_gridid, 0, 1, 10)

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
