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
from PyQt5.QtGui import QFont, QIntValidator, QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QFileDialog, QMessageBox

from lib.AppConfig import app_conf_get

class PhaseOutputWidget(QWidget):
    """Phase Output widget GUI"""

    def __init__(self, image_cache, i18n, log, cb_cancel, cb_next_phase):
        """Initializes the widget

        :param image_cache: The image cache
        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_cancel: Cancel callback
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseOutputWidget')

        self.image_cache = image_cache
        self.i18n = i18n
        self.log = log
        self.cb_cancel = cb_cancel
        self.cb_next_phase = cb_next_phase

        self.edit_image_size_width = None
        self.edit_image_size_height = None
        self.checkbox_create_pdf = None
        self.components = []

        self.edit_output_dir = None

        self.is_enabled = False

        self.output_dir = ''

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseOutputWidget GUI')

        font_label_header = QFont()
        font_label_header.setBold(True)
        font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        font_label_header_small = QFont()
        font_label_header_small.setBold(False)
        font_label_header_small.setPointSize(app_conf_get('label.header.small.font.size', 18))

        font_label_info = QFont()
        font_label_info.setBold(False)
        font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        font_label_info_small = QFont()
        font_label_info_small.setBold(False)
        font_label_info_small.setPointSize(app_conf_get('label.info.small.font.size', 12))

        line_css = 'background-color: #c0c0c0;'
        max_img_size_digits = 5

        # Components

        label_header = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.HEADER'))
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

        label_image_size = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE'))
        label_image_size.setFont(font_label_header_small)
        label_image_size.setAlignment(Qt.AlignLeft)

        label_image_size_width = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_WIDTH'))
        label_image_size_width.setFont(font_label_info)
        label_image_size_width.setAlignment(Qt.AlignLeft)

        label_image_size_px = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.PX'))
        label_image_size_px.setFont(font_label_info)
        label_image_size_px.setAlignment(Qt.AlignLeft)

        label_image_size_px2 = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.PX'))
        label_image_size_px2.setFont(font_label_info)
        label_image_size_px2.setAlignment(Qt.AlignLeft)

        label_image_size_times = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_TIMES'))
        label_image_size_times.setFont(font_label_info)
        label_image_size_times.setAlignment(Qt.AlignCenter)

        label_image_size_height = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_HEIGHT'))
        label_image_size_height.setFont(font_label_info)
        label_image_size_height.setAlignment(Qt.AlignLeft)

        self.edit_image_size_width = QLineEdit()
        self.edit_image_size_width.setValidator(QIntValidator())
        self.edit_image_size_width.setMaxLength(max_img_size_digits)
        self.edit_image_size_width.setText('1280')
        self.components.append(self.edit_image_size_width)

        self.edit_image_size_height = QLineEdit()
        self.edit_image_size_height.setValidator(QIntValidator())
        self.edit_image_size_height.setMaxLength(max_img_size_digits)
        self.edit_image_size_height.setText('')
        self.components.append(self.edit_image_size_height)

        label_image_size_info = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.IMAGE_SIZE_INFO'))
        label_image_size_info.setFont(font_label_info_small)
        label_image_size_info.setAlignment(Qt.AlignLeft)

        label_output_dir = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.OUTPUT_DIR'))
        label_output_dir.setFont(font_label_header_small)
        label_output_dir.setAlignment(Qt.AlignLeft)

        self.edit_output_dir = QLineEdit()
        self.edit_output_dir.setText(self.output_dir)
        self.edit_output_dir.setEnabled(False)

        button_output_dir = QPushButton(self.i18n.translate('GUI.PHASE.OUTPUT.BUTTON.SELECT_OUTPUT_DIR'))
        button_output_dir.clicked[bool].connect(self._select_output_dir)
        self.components.append(button_output_dir)

        label_pdf = QLabel(self.i18n.translate('GUI.PHASE.OUTPUT.LABEL.PDF'))
        label_pdf.setFont(font_label_header_small)
        label_pdf.setAlignment(Qt.AlignLeft)

        self.checkbox_create_pdf = QCheckBox(self.i18n.translate('GUI.PHASE.OUTPUT.CHECKBOX.CHECKBOX_CREATE_PDF'))
        self.checkbox_create_pdf.setChecked(True)
        self.components.append(self.checkbox_create_pdf)

        label_spacer = QLabel('')

        button_cancel = QPushButton(self.i18n.translate('GUI.PHASE.CANCEL'))
        button_cancel.clicked[bool].connect(self._cancel)
        self.components.append(button_cancel)

        button_next_phase = QPushButton(self.i18n.translate('GUI.PHASE.OUTPUT.NEXT_PHASE'))
        button_next_phase.clicked[bool].connect(self._next_phase)
        self.components.append(button_next_phase)

        # Layout

        grid = QGridLayout()
        grid.setSpacing(20)

        # grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        grid.addWidget(line_1, curr_gridid, 0, 1, 1)
        grid.addWidget(label_header, curr_gridid, 1, 1, 3)
        grid.addWidget(line_2, curr_gridid, 4, 1, 1)

        curr_gridid += 1
        grid.addWidget(label_image_size, curr_gridid, 0, 1, 5)

        curr_gridid += 1
        grid.addWidget(label_image_size_width, curr_gridid, 0, 1, 3)
        grid.addWidget(label_image_size_height, curr_gridid, 3, 1, 2)

        curr_gridid += 1
        grid.addWidget(self.edit_image_size_width, curr_gridid, 0, 1, 1)
        grid.addWidget(label_image_size_px, curr_gridid, 1, 1, 1)
        grid.addWidget(label_image_size_times, curr_gridid, 2, 1, 1)
        grid.addWidget(self.edit_image_size_height, curr_gridid, 3, 1, 1)
        grid.addWidget(label_image_size_px2, curr_gridid, 4, 1, 1)

        curr_gridid += 1
        grid.addWidget(label_image_size_info, curr_gridid, 0, 1, 5)

        curr_gridid += 1
        grid.addWidget(label_output_dir, curr_gridid, 0, 1, 1)

        curr_gridid += 1
        grid.addWidget(self.edit_output_dir, curr_gridid, 0, 1, 4)
        grid.addWidget(button_output_dir, curr_gridid, 4, 1, 1)

        curr_gridid += 1
        grid.addWidget(label_pdf, curr_gridid, 0, 1, 5)

        curr_gridid += 1
        grid.addWidget(self.checkbox_create_pdf, curr_gridid, 0, 1, 5)

        curr_gridid += 1
        grid.addWidget(label_spacer, curr_gridid, 0, 7, 5)

        curr_gridid += 8
        grid.addWidget(button_cancel, curr_gridid, 0, 1, 1)
        grid.addWidget(button_next_phase, curr_gridid, 1, 1, 4)

        self.setLayout(grid)
        self._reset_enabled()

    def set_images(self, images):
        """Sets images

        :param images: The images
        """
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
            logging.debug('Selected output directory: "%s"', dirname)
            self.output_dir = dirname
            self.edit_output_dir.setText(self.output_dir)
        else:
            self.log(self.i18n.translate('GUI.PHASE.OUTPUT.LOG.SELECT_OUTPUT_DIR_CANCEL'))
            logging.debug('Cancelled selecting output directory')

    def _cancel(self):
        """Cancels"""
        logging.debug('Cancel')

        if self.cb_cancel:
            self._disable()
            if not self.cb_cancel():
                self._reset_enabled()

    def _next_phase(self):
        """Netx phase"""
        logging.debug('Next phase')

        err = []
        if not self.edit_image_size_height.text() and not self.edit_image_size_width.text():
            err.append(self.i18n.translate('GUI.PHASE.OUTPUT.ERROR.IMAGE_SIZE'))
        if not self.output_dir:
            err.append(self.i18n.translate('GUI.PHASE.OUTPUT.ERROR.NO_OUTPUT_DIR_SELECTED'))
        if err:
            logging.debug('Errors: %s', err)
            msg = '<ul>'
            for _err in err:
                msg += f'<li>{_err}</li>'
            msg += '</ul>'
            msgbox = QMessageBox()
            logo = self.image_cache.get_or_load_pixmap('img.logo', 'logo.png')
            if logo is not None:
                msgbox.setWindowIcon(QIcon(logo))
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
