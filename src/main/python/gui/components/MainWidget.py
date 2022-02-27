#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Main widget"""

import logging
import os
import json
import csv

from PyQt5.QtCore import QThreadPool, Qt
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox

from lib.AppConfig import app_conf_get
from i18n.Translations import translate
from gui.components.ListWidget import ListWidget
from gui.threads.ScalerThread import ScalerThread


class MainWidget(QWidget):
    """Main widget GUI"""

    def __init__(self, log):
        """Initializes the main widget

        :param log: The (end user) message log
        """
        super().__init__()

        logging.debug('Initializing MainWidget')

        self.log = log
        self.components = []

        self.threadpool = QThreadPool()
        logging.debug('Multithreading with maximum {} threads.'.format(
            self.threadpool.maxThreadCount()))

        self.df_tenants = None
        self.output_dir = ''

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWidget GUI')

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(10)

        self.font_label_info = QFont()
        self.font_label_info.setBold(False)
        self.font_label_info.setPointSize(9)

        self.line_css = 'background-color: #c0c0c0;'
        self.max_img_size_digits = 5

        # Components

        self.label_select_images = QLabel(
            translate('GUI.MAIN.LABEL.INPUT'))
        self.label_select_images.setFont(self.font_label_header)
        self.label_select_images.setAlignment(Qt.AlignCenter)

        self.line_select_images_1 = QWidget()
        self.line_select_images_1.setFixedHeight(1)
        self.line_select_images_1.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_select_images_1.setStyleSheet(self.line_css)

        self.line_select_images_2 = QWidget()
        self.line_select_images_2.setFixedHeight(1)
        self.line_select_images_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_select_images_2.setStyleSheet(self.line_css)

        self.button_select_images = QPushButton(
            translate('GUI.MAIN.BUTTON.SELECT_IMAGES'))
        self.button_select_images.clicked[bool].connect(self._select_images)
        self.components.append(self.button_select_images)

        self.label_selected_images = QLabel(
            translate('GUI.MAIN.LABEL.SELECTED_IMAGES'))

        self.widget_list = QListWidget()
        self.widget_list.current_images = []

        self.label_settings = QLabel(
            translate('GUI.MAIN.LABEL.SETTINGS'))
        self.label_settings.setFont(self.font_label_header)
        self.label_settings.setAlignment(Qt.AlignCenter)

        self.line_settings_1 = QWidget()
        self.line_settings_1.setFixedHeight(1)
        self.line_settings_1.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_settings_1.setStyleSheet(self.line_css)

        self.line_settings_2 = QWidget()
        self.line_settings_2.setFixedHeight(1)
        self.line_settings_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_settings_2.setStyleSheet(self.line_css)

        self.label_image_size = QLabel(
            translate('GUI.MAIN.LABEL.IMAGE_SIZE'))

        self.label_image_size_width = QLabel(
            translate('GUI.MAIN.LABEL.IMAGE_SIZE_WIDTH'))

        self.label_image_size_times = QLabel(
            translate('GUI.MAIN.LABEL.IMAGE_SIZE_TIMES'))

        self.label_image_size_height = QLabel(
            translate('GUI.MAIN.LABEL.IMAGE_SIZE_HEIGHT'))

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

        self.label_image_size_info = QLabel(
            translate('GUI.MAIN.LABEL.IMAGE_SIZE_INFO'))
        self.label_image_size_info.setFont(self.font_label_info)

        self.label_output_dir = QLabel(
            translate('GUI.MAIN.LABEL.OUTPUT_DIR'))

        self.edit_output_dir = QLineEdit()
        self.edit_output_dir.setText(self.output_dir)
        self.edit_output_dir.setEnabled(False)

        self.button_output_dir = QPushButton(
            translate('GUI.MAIN.BUTTON.SELECT_OUTPUT_DIR'))
        self.button_output_dir.clicked[bool].connect(self._select_output_dir)
        self.components.append(self.button_output_dir)

        self.label_pdf = QLabel(
            translate('GUI.MAIN.LABEL.PDF'))
        self.checkbox_create_pdf = QCheckBox(translate('GUI.MAIN.CHECKBOX.CHECKBOX_CREATE_PDF'))
        self.checkbox_create_pdf.setChecked(True)
        self.components.append(self.checkbox_create_pdf)

        self.label_process = QLabel(
            translate('GUI.MAIN.LABEL.PROCESS'))
        self.label_process.setFont(self.font_label_header)
        self.label_process.setAlignment(Qt.AlignCenter)

        self.line_process_1 = QWidget()
        self.line_process_1.setFixedHeight(1)
        self.line_process_1.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_process_1.setStyleSheet(self.line_css)

        self.line_process_2 = QWidget()
        self.line_process_2.setFixedHeight(1)
        self.line_process_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_process_2.setStyleSheet(self.line_css)

        self.button_process = QPushButton(
            translate('GUI.MAIN.BUTTON.PROCESS'))
        self.button_process.clicked[bool].connect(self._start_processing)
        self.components.append(self.button_process)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 1
        self.grid.addWidget(self.line_select_images_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_select_images, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_select_images_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.button_select_images, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_selected_images, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.widget_list, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.line_settings_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_settings, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_settings_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.label_image_size, curr_gridid, 0, 1, 1)
        self.grid.addWidget(self.edit_image_size_width, curr_gridid, 1, 1, 3)
        self.grid.addWidget(self.label_image_size_width, curr_gridid, 4, 1, 1)
        self.grid.addWidget(self.label_image_size_times, curr_gridid, 5, 1, 1)
        self.grid.addWidget(self.edit_image_size_height, curr_gridid, 6, 1, 3)
        self.grid.addWidget(self.label_image_size_height, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self.label_image_size_info, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.label_output_dir, curr_gridid, 0, 1, 1)
        self.grid.addWidget(self.edit_output_dir, curr_gridid, 1, 1, 7)
        self.grid.addWidget(self.button_output_dir, curr_gridid, 8, 1, 2)

        curr_gridid += 1
        self.grid.addWidget(self.label_pdf, curr_gridid, 0, 1, 1)
        self.grid.addWidget(self.checkbox_create_pdf, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.line_process_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_process, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_process_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.button_process, curr_gridid, 0, 1, 10)

        self.setLayout(self.grid)
        self._reset_enabled()

    def _add_to_list(self, path_img):
        """Adds an item to the list

        :param img: The image
        """
        if path_img in self.widget_list.current_images:
            logging.debug(
                'Skipping adding image "{}" since it is already contained in list'.format(path_img))
            return
        logging.debug('Adding to list: "{}"'.format(path_img))
        try:
            with open(path_img) as f:
                fname = os.path.basename(f.name)
                item = QListWidgetItem(self.widget_list)
                item_widget = ListWidget(path_img, fname, self.widget_list)
                item.setSizeHint(item_widget.sizeHint())
                item.id = item_widget.id
                self.widget_list.addItem(item)
                self.widget_list.setItemWidget(item, item_widget)
                self.widget_list.current_images.append(path_img)
        except Exception as e:
            logging.error(
                'Error adding image "{}" to list: {}'.format(path_img, e))

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

    def _callback_processing_result(self, img_processed, img_cnt):
        """The processing callback, on result

        :param img_processed: Number of processed images
        :param img_cnt: Number of images
        """
        logging.debug('Callback: Processing result')

        self.log(translate('GUI.MAIN.LOG.DONE_PROCESSING').format(
            img_processed, img_cnt))

        self._reset_enabled()

    def _callback_processing_error(self, ex):
        """The processing callback, on error

        :param ex: The exception
        """
        logging.debug('Callback: Processing error')

        logging.error('Failed to process: "{}"'.format(ex))
        self.log('GUI.MAIN.LOG.ERROR_PROCESSING')

        self._reset_enabled()

    def _callback_processing_finished(self, img_processed, img_cnt):
        """The processing callback, on finished

        :param img_processed: Number of processed images
        :param img_cnt: Number of images
        """
        logging.debug('Callback: Processing finished')

        self.log(translate('GUI.MAIN.LOG.DONE_PROCESSING').format(
            img_processed, img_cnt))

        self._reset_enabled()

    def _select_images(self):
        """Selects images"""
        logging.debug('Selecting images')
        self.log(translate('GUI.MAIN.LOG.SELECT_IMAGES'))
        filter_mask = 'Image Files (*.jpeg *.jpg *.png)'
        filenames = QFileDialog.getOpenFileNames(
            self, translate('GUI.MAIN.DIALOG.SELECT'), './', filter_mask)[0]
        if filenames:
            self.log(
                translate('GUI.MAIN.LOG.SELECT_IMAGES_SUCCESS').format(len(filenames)))
            for fname in filenames:
                logging.debug('Selected file name: "{}"'.format(fname))
                self._add_to_list(fname)
        else:
            self.log(translate('GUI.MAIN.LOG.SELECT_IMAGES_CANCEL').format(0))
            logging.debug('Cancelled selecting files')

    def _select_output_dir(self):
        """Selects an output directory"""
        logging.debug('Selecting output directory')
        self.log(translate('GUI.MAIN.LOG.SELECT_OUTPUT_DIR'))
        dirname = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirname:
            self.log(
                translate('GUI.MAIN.LOG.SELECT_OUTPUT_DIR_SUCCESS').format(dirname))
            logging.debug('Selected output directory: "{}"'.format(dirname))
            self.output_dir = dirname
            self.edit_output_dir.setText(self.output_dir)
        else:
            self.log(translate('GUI.MAIN.LOG.SELECT_OUTPUT_DIR_CANCEL'))
            logging.debug('Cancelled selecting output directory')

    def _start_processing(self):
        """Starts processing"""
        logging.debug('Start processing')
        err = []
        if not self.edit_image_size_height.text() and not self.edit_image_size_width.text():
            err.append(translate('GUI.MAIN.ERROR.IMAGE_SIZE'))
        if not self.output_dir:
            err.append(translate('GUI.MAIN.ERROR.NO_OUTPUT_DIR_SELECTED'))
        if not self.widget_list.current_images:
            err.append(translate('GUI.MAIN.ERROR.NO_IMAGES_SELECTED'))
        if err:
            logging.debug('Errors: {}'.format(err))
            msg = '<ul>'
            for e in err:
                msg += '<li>{}</li>'.format(e)
            msg += '</ul>'
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(translate('GUI.MAIN.ERROR.START_PROCESSING'))
            msgbox.setInformativeText(msg)
            msgbox.setWindowTitle(translate('GUI.MAIN.ERROR.ERROR'))
            msgbox.exec_()
        else:
            self._disable()

            try:
                logging.debug('Starting processing')
                self.log(translate('GUI.MAIN.LOG.START_PROCESSING'))

                images = self.widget_list.current_images
                width = int(self.edit_image_size_width.text(
                )) if self.edit_image_size_width.text() else None
                height = int(self.edit_image_size_height.text(
                )) if self.edit_image_size_height.text() else None
                outdir = self.output_dir
                thread = ScalerThread(
                    images=images, width=width, height=height, outdir=outdir, createpdf=self.checkbox_create_pdf.isChecked())
                thread.signals.scalingresult.connect(
                    self._callback_processing_result)
                thread.signals.scalingerror.connect(
                    self._callback_processing_error)
                thread.signals.scalingfinished.connect(
                    self._callback_processing_finished)
                self.threadpool.start(thread)
            except Exception as e:
                logging.debug('Error while scaling: {}'.format(e))
                self.log('GUI.MAIN.LOG.ERROR_PROCESSING')
                self._reset_enabled()
