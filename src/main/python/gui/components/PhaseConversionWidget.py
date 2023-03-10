#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Phase Conversion widget"""

import logging

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QPushButton, QMessageBox, QProgressBar

from gui.threads.ScalerThread import ScalerThread
from lib.AppConfig import app_conf_get

class PhaseConversionWidget(QWidget):
    """Phase Conversion widget GUI"""

    def __init__(self, i18n, log, cb_cancel, cb_next_phase):
        """Initializes the widget

        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_cancel: Cancel callback
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseConversionWidget')

        self.i18n = i18n
        self.log = log
        self.cb_cancel = cb_cancel
        self.cb_next_phase = cb_next_phase

        self.components = []

        self.images = []
        self.config = {}
        self.pdf_written = False

        self.img_processed = 0
        self.img_cnt = 0

        self.threadpool = QThreadPool()
        logging.debug('Multithreading with maximum {} threads.'.format(self.threadpool.maxThreadCount()))

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseConversionWidget GUI')

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

        # Components

        self.label_header = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.HEADER'))
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

        self.label_images = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGES'))
        self.label_images.setFont(self.font_label_header_small)
        self.label_images.setAlignment(Qt.AlignLeft)

        nr_images = len(self.images) if self.images else 0
        self.label_images_text = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGES.TEXT').format(nr_images))
        self.label_images_text.setFont(self.font_label_info)
        self.label_images_text.setAlignment(Qt.AlignLeft)

        self.label_image_size = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE'))
        self.label_image_size.setFont(self.font_label_header_small)
        self.label_image_size.setAlignment(Qt.AlignLeft)

        txt_width = self.config['IMG_WIDTH'] if ('IMG_WIDTH' in self.config and self.config['IMG_WIDTH']) else '-'
        self.label_image_size_width = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_WIDTH').format(txt_width))
        self.label_image_size_width.setFont(self.font_label_info)
        self.label_image_size_width.setAlignment(Qt.AlignLeft)

        txt_height = self.config['IMG_HEIGHT'] if ('IMG_HEIGHT' in self.config and self.config['IMG_HEIGHT']) else '-'
        self.label_image_size_height = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_HEIGHT').format(txt_height))
        self.label_image_size_height.setFont(self.font_label_info)
        self.label_image_size_height.setAlignment(Qt.AlignLeft)

        self.label_image_size_info = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_INFO'))
        self.label_image_size_info.setFont(self.font_label_info_small)
        self.label_image_size_info.setAlignment(Qt.AlignLeft)

        self.label_output_dir = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.OUTPUT_DIR'))
        self.label_output_dir.setFont(self.font_label_header_small)
        self.label_output_dir.setAlignment(Qt.AlignLeft)

        txt_outdir = self.config['OUTPUT_DIR'] if ('OUTPUT_DIR' in self.config and self.config['OUTPUT_DIR']) else '-'
        self.label_output_dir_value = QLabel(txt_outdir)
        self.label_output_dir_value.setFont(self.font_label_info)
        self.label_output_dir_value.setAlignment(Qt.AlignLeft)

        self.label_pdf = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.PDF'))
        self.label_pdf.setFont(self.font_label_header_small)
        self.label_pdf.setAlignment(Qt.AlignLeft)

        self.label_pdf_text = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.PDF.TEXT'))
        self.label_pdf_text.setFont(self.font_label_info)
        self.label_pdf_text.setAlignment(Qt.AlignLeft)

        self.label_no_pdf_text = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.NO_PDF.TEXT'))
        self.label_no_pdf_text.setFont(self.font_label_info)
        self.label_no_pdf_text.setAlignment(Qt.AlignLeft)

        self.label_spacer = QLabel('')

        self.button_cancel = QPushButton(self.i18n.translate('GUI.PHASE.CANCEL'))
        self.button_cancel.clicked[bool].connect(self._cancel)
        self.components.append(self.button_cancel)

        self.button_start = QPushButton(self.i18n.translate('GUI.PHASE.CONVERSION.BUTTON.PROCESS'))
        self.button_start.clicked[bool].connect(self._start_processing)
        self.components.append(self.button_start)

        self.progressbar = QProgressBar()

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)
        
        curr_gridid = 1
        self.grid.addWidget(self.line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_header, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.label_images, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        self.grid.addWidget(self.label_images_text, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.label_image_size, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        self.grid.addWidget(self.label_image_size_width, curr_gridid, 1, 1, 9)
        curr_gridid += 1
        self.grid.addWidget(self.label_image_size_height, curr_gridid, 1, 1, 9)
        curr_gridid += 1
        self.grid.addWidget(self.label_image_size_info, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.label_output_dir, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        self.grid.addWidget(self.label_output_dir_value, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.label_pdf, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        if self.config['CREATE_PDF'] if 'CREATE_PDF' in self.config else True:
            self.grid.addWidget(self.label_pdf_text, curr_gridid, 1, 1, 9)
        else:
            self.grid.addWidget(self.label_no_pdf_text, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        self.grid.addWidget(self.label_spacer, curr_gridid, 0, 7, 10)

        curr_gridid += 8
        self.grid.addWidget(self.progressbar, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.button_cancel, curr_gridid, 0, 1, 2)
        self.grid.addWidget(self.button_start, curr_gridid, 2, 1, 8)

        self.setLayout(self.grid)
        self._reset_enabled()

    def reset(self):
        """Resets the widget"""
        logging.debug('Resetting widget')

        self.progressbar.reset()
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

    def _callback_processing_result(self, img_processed, img_cnt):
        """The processing callback, on result

        :param img_processed: Number of processed images
        :param img_cnt: Number of images
        """
        logging.debug('Callback: Processing result')

        self.log(self.i18n.translate('GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.{}'.format('SINGULAR' if img_processed == 1 else 'PLURAL')).format(img_processed, img_cnt))

        self._reset_enabled()

    def _callback_processing_error(self, ex):
        """The processing callback, on error

        :param ex: The exception
        """
        logging.debug('Callback: Processing error')

        logging.error('Failed to process: "{}"'.format(ex))
        self.log(self.i18n.translate('GUI.PHASE.CONVERSION.LOG.ERROR_PROCESSING'))

        self._reset_enabled()

    def _cancel(self):
        """Cancels"""
        logging.debug('Cancel')

        if self.cb_cancel:
            self._disable()
            self.cb_cancel()

    def _callback_processing_finished(self, img_processed, img_cnt, pdf_written):
        """The processing callback, on finished

        :param img_processed: Number of processed images
        :param img_cnt: Number of images
        :param pdf_written: Boolean flag whether a PDF file has been written
        """
        logging.debug('Callback: Processing finished')

        self.img_processed = img_processed
        self.img_cnt = img_cnt
        self.pdf_written = pdf_written
        self.log(self.i18n.translate('GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.{}.{}'
                                     .format('SINGULAR' if img_processed == 1 else 'PLURAL', 'PDF' if pdf_written else 'NO_PDF'))
                                     .format(img_processed, img_cnt))

        self._reset_enabled()

        if self.cb_next_phase:
            self.cb_next_phase()

    def _start_processing(self):
        """Starts processing"""
        logging.debug('Start processing')
        err = []
        if not ('IMG_HEIGHT' in self.config and self.config['IMG_HEIGHT']) and not ('IMG_WIDTH' in self.config and self.config['IMG_WIDTH']):
            err.append(self.i18n.translate('GUI.PHASE.CONVERSION.ERROR.IMAGE_SIZE'))
        if not ('OUTPUT_DIR' in self.config and self.config['OUTPUT_DIR']):
            err.append(self.i18n.translate('GUI.PHASE.CONVERSION.ERROR.NO_OUTPUT_DIR_SELECTED'))
        if not self.images:
            err.append(self.i18n.translate('GUI.PHASE.CONVERSION.ERROR.NO_IMAGES_SELECTED'))
        if err:
            logging.debug('Errors: {}'.format(err))
            msg = '<ul>'
            for e in err:
                msg += '<li>{}</li>'.format(e)
            msg += '</ul>'
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(self.i18n.translate('GUI.PHASE.CONVERSION.ERROR.START_PROCESSING'))
            msgbox.setInformativeText(msg)
            msgbox.setWindowTitle(self.i18n.translate('GUI.PHASE.CONVERSION.ERROR.ERROR'))
            msgbox.exec_()
        else:
            self._disable()

            self.progressbar.setMinimum(0)
            self.progressbar.setMaximum(0)

            try:
                logging.debug('Starting processing')
                self.log(self.i18n.translate('GUI.PHASE.CONVERSION.LOG.START_PROCESSING'))

                if 'IMG_WIDTH' in self.config and self.config['IMG_WIDTH']:
                    width = int(self.config['IMG_WIDTH'])
                else:
                    width = None
                if 'IMG_HEIGHT' in self.config and self.config['IMG_HEIGHT']:
                    height = int(self.config['IMG_HEIGHT'])
                else:
                    height = None
                outdir = self.config['OUTPUT_DIR']
                thread = ScalerThread(
                    images=self.images,
                    width=width,
                    height=height,
                    outdir=outdir,
                    createpdf=self.config['CREATE_PDF'] if 'CREATE_PDF' in self.config else True,
                    scaled_image_suffix=self.i18n.translate('SCALED_IMAGE_SUFFIX'),
                    pdf_name=self.i18n.translate('PDF.NAME'))
                thread.signals.scalingresult.connect(self._callback_processing_result)
                thread.signals.scalingerror.connect(self._callback_processing_error)
                thread.signals.scalingfinished.connect(self._callback_processing_finished)
                self.threadpool.start(thread)
            except Exception as e:
                logging.debug('Error while scaling: {}'.format(e))
                self.log('GUI.PHASE.CONVERSION.LOG.ERROR_PROCESSING')
                self._reset_enabled()

    def set_config(self, images, config):
        """Sets the config

        :param images: The images (list)
        :param config: The config (map)
        """
        self.images = images
        self.config = config

    def get_nr_converted_images(self):
        """Returns the number of converted images

        :return: The number of converted images
        """
        return self.img_processed

    def get_nr_all_images(self):
        """Returns the number of all images

        :return: The number of all images
        """
        return self.img_cnt

    def isPdfWritten(self):
        """Returns whether a PDF file has been written

        :return: Boolean flag whether a PDF file has been written
        """
        return self.pdf_written
