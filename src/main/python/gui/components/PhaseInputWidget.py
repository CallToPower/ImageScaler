#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Phase Input widget"""

import logging
import os

import filetype

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView, QSizePolicy, QWidget, QGridLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox

from gui.components.ListWidget import ListWidget

from lib.AppConfig import app_conf_get


class PhaseInputWidget(QWidget):
    """Phase Input widget GUI"""

    def __init__(self, i18n, log, cb_cancel, cb_next_phase):
        """Initializes the widget

        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_cancel: Cancel callback
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseInputWidget')

        self.i18n = i18n
        self.log = log
        self.cb_cancel = cb_cancel
        self.cb_next_phase = cb_next_phase

        self.widget_list = None
        self.components = []

        self.setAcceptDrops(True)

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseInputWidget GUI')

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        self.font_label_header_small = QFont()
        self.font_label_header_small.setBold(False)
        self.font_label_header_small.setPointSize(app_conf_get('label.header.small.font.size', 18))

        self.font_label_info_small = QFont()
        self.font_label_info_small.setBold(False)
        self.font_label_info_small.setPointSize(app_conf_get('label.info.small.font.size', 10))

        self.line_css = 'background-color: #c0c0c0;'
        self.max_img_size_digits = 5

        # Components

        self.label_header = QLabel(self.i18n.translate('GUI.PHASE.INPUT.HEADER'))
        self.label_header.setFont(self.font_label_header)
        self.label_header.setAlignment(Qt.AlignCenter)

        self.line_select_images_1 = QWidget()
        self.line_select_images_1.setFixedHeight(1)
        self.line_select_images_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_select_images_1.setStyleSheet(self.line_css)

        self.line_select_images_2 = QWidget()
        self.line_select_images_2.setFixedHeight(1)
        self.line_select_images_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_select_images_2.setStyleSheet(self.line_css)

        self.button_select_images = QPushButton(self.i18n.translate('GUI.PHASE.INPUT.SELECT_IMAGES'))
        self.button_select_images.clicked[bool].connect(self._select_images)
        self.components.append(self.button_select_images)

        self.label_dragndrop_hint = QLabel(self.i18n.translate('GUI.PHASE.INPUT.HINT'))
        self.label_dragndrop_hint.setFont(self.font_label_info_small)
        self.label_dragndrop_hint.setAlignment(Qt.AlignCenter)

        self.label_selected_images = QLabel(self.i18n.translate('GUI.PHASE.INPUT.SELECTED_IMAGES'))
        self.label_selected_images.setFont(self.font_label_header_small)
        self.label_selected_images.setAlignment(Qt.AlignLeft)

        self.label_selected_images_hint = QLabel(self.i18n.translate('GUI.PHASE.INPUT.SELECTED_IMAGES.HINT'))
        self.label_selected_images_hint.setFont(self.font_label_info_small)
        self.label_selected_images_hint.setAlignment(Qt.AlignLeft)

        self.widget_list = QListWidget()
        self.widget_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.widget_list.model().rowsMoved.connect(self._item_moved)
        self.widget_list.current_images = []

        self.button_cancel = QPushButton(self.i18n.translate('GUI.PHASE.CANCEL'))
        self.button_cancel.clicked[bool].connect(self._cancel)
        self.components.append(self.button_cancel)

        self.button_next_phase = QPushButton(self.i18n.translate('GUI.PHASE.INPUT.NEXT_PHASE'))
        self.button_next_phase.clicked[bool].connect(self._next_phase)
        self.components.append(self.button_next_phase)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 1
        self.grid.addWidget(self.line_select_images_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_header, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_select_images_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.button_select_images, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_dragndrop_hint, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_selected_images, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.label_selected_images_hint, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.widget_list, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.button_cancel, curr_gridid, 0, 1, 2)
        self.grid.addWidget(self.button_next_phase, curr_gridid, 2, 1, 8)

        self.setLayout(self.grid)
        self._reset_enabled()

    def _item_moved(self, _i1, i_from, _i2, _i3, i_to):
        if len(self.widget_list.current_images) > 1:
            _imgs = self.widget_list.current_images
            elem = _imgs[i_from]
            _imgs.insert(i_to, elem)
            for i, el in enumerate(_imgs):
                if i != i_to and el == elem:
                    _imgs.pop(i)
                    return

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

    def _filter_image_files(self, event):
        filetypes = ['image/jpeg', 'image/png']
        lst = []
        for u in event.mimeData().urls():
            t = filetype.guess(u.toLocalFile())
            if t and t.mime in filetypes:
                lst.append(u.toLocalFile())
        return lst

    def dragEnterEvent(self, event):
        if self._filter_image_files(event):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = self._filter_image_files(event)
        for file in files:
            self._add_to_list(file)
        if files:
            event.accept()
        else:
            event.ignore()

    def _add_to_list(self, path_img):
        """Adds an item to the list

        :param img: The image
        """
        if path_img in self.widget_list.current_images:
            logging.debug('Skipping adding image "{}" since it is already contained in list'.format(path_img))
            return
        logging.debug('Adding to list: "{}"'.format(path_img))
        try:
            with open(path_img) as f:
                fname = os.path.basename(f.name)
                item = QListWidgetItem(self.widget_list)
                item_widget = ListWidget(self.i18n, path_img, fname, self.widget_list)
                item.setSizeHint(item_widget.sizeHint())
                item.id = item_widget.id
                self.widget_list.addItem(item)
                self.widget_list.setItemWidget(item, item_widget)
                self.widget_list.current_images.append(path_img)
        except Exception as e:
            logging.error('Error adding image "{}" to list: {}'.format(path_img, e))

    def _select_images(self):
        """Selects images"""
        logging.debug('Selecting images')
        self.log(self.i18n.translate('GUI.PHASE.INPUT.LOG.SELECT_IMAGES'))
        filter_mask = 'Image Files (*.jpeg *.jpg *.png)'
        filenames = QFileDialog.getOpenFileNames(self, self.i18n.translate('GUI.PHASE.INPUT.DIALOG.SELECT'), './', filter_mask)[0]
        if filenames:
            self.log(self.i18n.translate('GUI.PHASE.INPUT.LOG.SELECT_IMAGES_SUCCESS').format(len(filenames)))
            for fname in filenames:
                if filetype.is_image(fname):
                    logging.debug('Selected file name: "{}"'.format(fname))
                    self._add_to_list(fname)
        else:
            self.log(self.i18n.translate('GUI.PHASE.INPUT.LOG.SELECT_IMAGES_CANCEL').format(0))
            logging.debug('Cancelled selecting files')

    def _cancel(self):
        """Cancels"""
        logging.debug('Cancel')

        if self.cb_cancel:
            self._disable()
            self.cb_cancel()

    def _next_phase(self):
        """Goes to the next phase"""
        logging.debug('Next phase')

        err = []
        if not self.widget_list.current_images:
            err.append(self.i18n.translate('GUI.PHASE.INPUT.ERROR.NO_IMAGES_SELECTED'))
        if err:
            logging.debug('Errors: {}'.format(err))
            msg = '<ul>'
            for e in err:
                msg += '<li>{}</li>'.format(e)
            msg += '</ul>'
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(self.i18n.translate('GUI.PHASE.INPUT.ERROR.NEXT_PHASE'))
            msgbox.setInformativeText(msg)
            msgbox.setWindowTitle(self.i18n.translate('GUI.PHASE.INPUT.ERROR.ERROR'))
            msgbox.exec_()
        else:
            if self.cb_next_phase:
                self._disable()
                self.cb_next_phase()

    def get_selected_images(self):
        """Returns selected images
        
        :return: Selected images
        """
        if not self.widget_list:
            return []
        return self.widget_list.current_images
