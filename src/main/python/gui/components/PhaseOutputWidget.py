#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Phase Output widget"""

import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QFileDialog, QMessageBox

from lib.AppConfig import app_conf_get


class PhaseOutputWidget(QWidget):
    """Phase Output widget GUI"""

    def __init__(self, i18n, log, cb_next_phase):
        """Initializes the widget

        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseOutputWidget')

        self.i18n = i18n
        self.log = log
        self.cb_next_phase = cb_next_phase

        self.edit_image_size_width = None
        self.edit_image_size_height = None
        self.checkbox_create_pdf = None
        self.components = []

        self.output_dir = ''

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseOutputWidget GUI')

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        self.font_label_header_small = QFont()
        self.font_label_header_small.setBold(False)
        self.font_label_header_small.setPointSize(app_conf_get('label.header.small.font.size', 18))

        self.font_label_info = QFont()
        self.font_label_info.setBold(False)
        self.font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        self.font_label_info_small = QFont()
        self.font_label_info_small.setBold(False)
        self.font_label_info_small.setPointSize(app_conf_get('label.info.small.font.size', 12))

        self.line_css = 'background-color: #c0c0c0;'
        self.max_img_size_digits = 5

        # Components

        self.label_header = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.HEADER'))
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

        self.label_image_size = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE'))
        self.label_image_size.setFont(self.font_label_header_small)
        self.label_image_size.setAlignment(Qt.AlignLeft)

        self.label_image_size_width = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_WIDTH'))
        self.label_image_size_width.setFont(self.font_label_info)
        self.label_image_size_width.setAlignment(Qt.AlignLeft)

        self.label_image_size_times = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_TIMES'))
        self.label_image_size_times.setFont(self.font_label_info)
        self.label_image_size_times.setAlignment(Qt.AlignCenter)

        self.label_image_size_height = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_HEIGHT'))
        self.label_image_size_height.setFont(self.font_label_info)
        self.label_image_size_height.setAlignment(Qt.AlignLeft)

        self.edit_image_size_width = QLineEdit()
        self.edit_image_size_width.setValidator(QIntValidator())
        self.edit_image_size_width.setMaxLength(self.max_img_size_digits)
        self.edit_image_size_width.setText('1280')
        self.components.append(self.edit_image_size_width)

        self.edit_image_size_height = QLineEdit()
        self.edit_image_size_height.setValidator(QIntValidator())
        self.edit_image_size_height.setMaxLength(self.max_img_size_digits)
        self.edit_image_size_height.setText('')
        self.components.append(self.edit_image_size_height)

        self.label_image_size_info = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_INFO'))
        self.label_image_size_info.setFont(self.font_label_info_small)
        self.label_image_size_info.setAlignment(Qt.AlignLeft)

        self.label_output_dir = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.OUTPUT_DIR'))
        self.label_output_dir.setFont(self.font_label_header_small)
        self.label_output_dir.setAlignment(Qt.AlignLeft)

        self.edit_output_dir = QLineEdit()
        self.edit_output_dir.setText(self.output_dir)
        self.edit_output_dir.setEnabled(False)

        self.button_output_dir = QPushButton(self.i18n.translate('GUI.PHASE.OUTPUT.BUTTON.SELECT_OUTPUT_DIR'))
        self.button_output_dir.clicked[bool].connect(self._select_output_dir)
        self.components.append(self.button_output_dir)

        self.label_pdf = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.PDF'))
        self.label_pdf.setFont(self.font_label_header_small)
        self.label_pdf.setAlignment(Qt.AlignLeft)

        self.checkbox_create_pdf = QCheckBox(self.i18n.translate('GUI.PHASE.OUTPUT.CHECKBOX.CHECKBOX_CREATE_PDF'))
        self.checkbox_create_pdf.setChecked(True)
        self.components.append(self.checkbox_create_pdf)

        self.label_spacer = QLabel('')

        self.button_next_phase = QPushButton(self.i18n.translate('GUI.PHASE.OUTPUT.NEXT_PHASE'))
        self.button_next_phase.clicked[bool].connect(self._next_phase)
        self.components.append(self.button_next_phase)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 1
        self.grid.addWidget(self.line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_header, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.label_image_size, curr_gridid, 0, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self.edit_image_size_width, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_image_size_width, curr_gridid, 3, 1, 1)
        self.grid.addWidget(self.label_image_size_times, curr_gridid, 4, 1, 1)
        self.grid.addWidget(self.edit_image_size_height, curr_gridid, 5, 1, 4)
        self.grid.addWidget(self.label_image_size_height, curr_gridid, 8, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self.label_image_size_info, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_output_dir, curr_gridid, 0, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self.edit_output_dir, curr_gridid, 0, 1, 7)
        self.grid.addWidget(self.button_output_dir, curr_gridid, 7, 1, 3)

        curr_gridid += 1
        self.grid.addWidget(self.label_pdf, curr_gridid, 0, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self.checkbox_create_pdf, curr_gridid, 0, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.label_spacer, curr_gridid, 0, 7, 10)

        curr_gridid += 8
        self.grid.addWidget(self.button_next_phase, curr_gridid, 0, 1, 10)

        self.setLayout(self.grid)
        self._reset_enabled()

    def set_images(self, images):
        if images:
            self.output_dir = os.path.dirname(images[0])

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

    def _select_output_dir(self):
        """Selects an output directory"""
        logging.debug('Selecting output directory')
        self.log(self.i18n.translate('GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR'))
        dirname = QFileDialog.getExistingDirectory(self, "Select Directory", self.output_dir)
        if dirname:
            self.log(self.i18n.translate('GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_SUCCESS').format(dirname))
            logging.debug('Selected output directory: "{}"'.format(dirname))
            self.output_dir = dirname
            self.edit_output_dir.setText(self.output_dir)
        else:
            self.log(self.i18n.translate('GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_CANCEL'))
            logging.debug('Cancelled selecting output directory')

    def _next_phase(self):
        """Netx phase"""
        logging.debug('Next phase')

        err = []
        if not self.edit_image_size_height.text() and not self.edit_image_size_width.text():
            err.append(self.i18n.translate('GUI.PHASE.OUTPUT.ERROR.IMAGE_SIZE'))
        if not self.output_dir:
            err.append(self.i18n.translate('GUI.PHASE.OUTPUT.ERROR.NO_OUTPUT_DIR_SELECTED'))
        if err:
            logging.debug('Errors: {}'.format(err))
            msg = '<ul>'
            for e in err:
                msg += '<li>{}</li>'.format(e)
            msg += '</ul>'
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(self.i18n.translate('GUI.PHASE.OUTPUT.ERROR.NEXT_PHASE'))
            msgbox.setInformativeText(msg)
            msgbox.setWindowTitle(self.i18n.translate('GUI.PHASE.OUTPUT.ERROR.ERROR'))
            msgbox.exec_()
        else:
            if self.cb_next_phase:
                self._disable()
                self.cb_next_phase()

    def get_config(self):
        """Returns the config

        :return: The config
        """
        return {
            'OUTPUT_DIR': self.output_dir,
            'IMG_WIDTH': self.edit_image_size_width.text() if self.edit_image_size_width else '',
            'IMG_HEIGHT': self.edit_image_size_height.text() if self.edit_image_size_height else '',
            'CREATE_PDF': self.checkbox_create_pdf.isChecked() if self.checkbox_create_pdf else True
        }
