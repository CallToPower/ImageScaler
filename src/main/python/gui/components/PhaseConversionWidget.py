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
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QPushButton, QMessageBox, QProgressBar

from gui.threads.ScalerThread import ScalerThread
from lib.AppConfig import app_conf_get

class PhaseConversionWidget(QWidget):
    """Phase Conversion widget GUI"""

    def __init__(self, image_cache, i18n, log, cb_cancel, cb_next_phase):
        """Initializes the widget

        :param image_cache: The image cache
        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_cancel: Cancel callback
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseConversionWidget')

        self.image_cache = image_cache
        self.i18n = i18n
        self.log = log
        self.cb_cancel = cb_cancel
        self.cb_next_phase = cb_next_phase

        self.components = []
        self.progressbar = None

        self.images = []
        self.config = {}
        self.pdf_written = False

        self.img_processed = 0
        self.img_cnt = 0

        self.is_enabled = False

        self.threadpool = QThreadPool()
        logging.debug('Multithreading with maximum %d threads.', self.threadpool.maxThreadCount())

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseConversionWidget GUI')

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

        # Components

        label_header = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.HEADER'))
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

        label_images = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGES'))
        label_images.setFont(font_label_header_small)
        label_images.setAlignment(Qt.AlignLeft)

        nr_images = len(self.images) if self.images else 0
        label_images_text = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGES.TEXT').format(nr_images))
        label_images_text.setFont(font_label_info)
        label_images_text.setAlignment(Qt.AlignLeft)

        label_image_size = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE'))
        label_image_size.setFont(font_label_header_small)
        label_image_size.setAlignment(Qt.AlignLeft)

        txt_width = self.config['IMG_WIDTH'] if ('IMG_WIDTH' in self.config and self.config['IMG_WIDTH']) else '-'
        label_image_size_width = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_WIDTH').format(txt_width))
        label_image_size_width.setFont(font_label_info)
        label_image_size_width.setAlignment(Qt.AlignLeft)

        txt_height = self.config['IMG_HEIGHT'] if ('IMG_HEIGHT' in self.config and self.config['IMG_HEIGHT']) else '-'
        label_image_size_height = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_HEIGHT').format(txt_height))
        label_image_size_height.setFont(font_label_info)
        label_image_size_height.setAlignment(Qt.AlignLeft)

        _size_info_addition = '.HEIGHT' if ('IMG_WIDTH' in self.config and self.config['IMG_WIDTH']) else '.WIDTH'
        label_image_size_info = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.IMAGE_SIZE_INFO' + _size_info_addition))
        label_image_size_info.setFont(font_label_info_small)
        label_image_size_info.setAlignment(Qt.AlignLeft)

        label_output_dir = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.OUTPUT_DIR'))
        label_output_dir.setFont(font_label_header_small)
        label_output_dir.setAlignment(Qt.AlignLeft)

        txt_outdir = self.config['OUTPUT_DIR'] if ('OUTPUT_DIR' in self.config and self.config['OUTPUT_DIR']) else '-'
        label_output_dir_value = QLabel(txt_outdir)
        label_output_dir_value.setFont(font_label_info)
        label_output_dir_value.setAlignment(Qt.AlignLeft)

        label_pdf = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.PDF'))
        label_pdf.setFont(font_label_header_small)
        label_pdf.setAlignment(Qt.AlignLeft)

        label_pdf_text = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.PDF.TEXT'))
        label_pdf_text.setFont(font_label_info)
        label_pdf_text.setAlignment(Qt.AlignLeft)

        label_no_pdf_text = QLabel(self.i18n.translate('GUI.PHASE.CONVERSION.LABEL.NO_PDF.TEXT'))
        label_no_pdf_text.setFont(font_label_info)
        label_no_pdf_text.setAlignment(Qt.AlignLeft)

        label_spacer = QLabel('')

        button_cancel = QPushButton(self.i18n.translate('GUI.PHASE.CANCEL'))
        button_cancel.clicked[bool].connect(self._cancel)
        self.components.append(button_cancel)

        button_start = QPushButton(self.i18n.translate('GUI.PHASE.CONVERSION.BUTTON.PROCESS'))
        button_start.clicked[bool].connect(self._start_processing)
        self.components.append(button_start)

        self.progressbar = QProgressBar()

        # Layout

        grid = QGridLayout()
        grid.setSpacing(20)

        # grid.addWidget(widget, row, column, rowspan, columnspan)
        
        curr_gridid = 0
        grid.addWidget(line_1, curr_gridid, 0, 1, 4)
        grid.addWidget(label_header, curr_gridid, 4, 1, 2)
        grid.addWidget(line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        grid.addWidget(label_images, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        grid.addWidget(label_images_text, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        grid.addWidget(label_image_size, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        grid.addWidget(label_image_size_width, curr_gridid, 1, 1, 9)
        curr_gridid += 1
        grid.addWidget(label_image_size_height, curr_gridid, 1, 1, 9)
        has_width = 'IMG_WIDTH' in self.config and self.config['IMG_WIDTH']
        has_height = 'IMG_HEIGHT' in self.config and self.config['IMG_HEIGHT']
        if (has_width and not has_height) or (has_height and not has_width):
            curr_gridid += 1
            grid.addWidget(label_image_size_info, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        grid.addWidget(label_output_dir, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        grid.addWidget(label_output_dir_value, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        grid.addWidget(label_pdf, curr_gridid, 0, 1, 10)
        curr_gridid += 1
        if self.config['CREATE_PDF'] if 'CREATE_PDF' in self.config else True:
            grid.addWidget(label_pdf_text, curr_gridid, 1, 1, 9)
        else:
            grid.addWidget(label_no_pdf_text, curr_gridid, 1, 1, 9)

        curr_gridid += 1
        grid.addWidget(label_spacer, curr_gridid, 0, 7, 10)

        curr_gridid += 8
        grid.addWidget(self.progressbar, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        grid.addWidget(button_cancel, curr_gridid, 0, 1, 4)
        grid.addWidget(button_start, curr_gridid, 4, 1, 6)

        self.setLayout(grid)
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
        logging.info('Disabling components')

        self.is_enabled = False
        for comp in self.components:
            comp.setEnabled(False)

    def _enable(self):
        """Resets all component to enabled state"""
        logging.info('Enabling components')

        for comp in self.components:
            comp.setEnabled(True)
        self.is_enabled = True

    def _callback_processing_result(self, img_processed, img_cnt):
        """The processing callback, on result

        :param img_processed: Number of processed images
        :param img_cnt: Number of images
        """
        logging.debug('Callback: Processing result')

        self.log(self.i18n.translate(f'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.{"SINGULAR" if img_processed == 1 else "PLURAL"}')
                                     .format(img_processed, img_cnt))

    def _callback_processing_error(self, ex):
        """The processing callback, on error

        :param ex: The exception
        """
        logging.debug('Callback: Processing error')

        logging.error('Failed to process: "%s"', ex)
        self.log(self.i18n.translate('GUI.PHASE.CONVERSION.LOG.ERROR_PROCESSING'))

        self._reset_enabled()

    def _cancel(self):
        """Cancels"""
        logging.debug('Cancel')

        if self.cb_cancel:
            self._disable()
            if not self.cb_cancel():
                self._reset_enabled()

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
        self.log(self.i18n.translate(f'GUI.PHASE.CONVERSION.LOG.DONE_PROCESSING.{"SINGULAR" if img_processed == 1 else "PLURAL"}.{"PDF" if pdf_written else "NO_PDF"}')
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
            logging.debug('Errors: %s', err)
            msg = '<ul>'
            for err in err:
                msg += f'<li>{err}</li>'
            msg += '</ul>'
            msgbox = QMessageBox()
            logo = self.image_cache.get_or_load_pixmap('img.logo', 'logo.png')
            if logo is not None:
                msgbox.setWindowIcon(QIcon(logo))
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
            except Exception as ex:
                logging.debug('Error while scaling: %s', ex)
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

    def is_pdf_written(self):
        """Returns whether a PDF file has been written

        :return: Boolean flag whether a PDF file has been written
        """
        return self.pdf_written
