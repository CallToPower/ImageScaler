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
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QAbstractItemView, QSizePolicy, QWidget, QGridLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox

from gui.components.ListWidget import ListWidget
from lib.AppConfig import app_conf_get

class PhaseInputWidget(QWidget):
    """Phase Input widget GUI"""

    def __init__(self, image_cache, i18n, log, cb_cancel, cb_next_phase):
        """Initializes the widget

        :param image_cache: The image cache
        :param i18n: The I18n
        :param log: The (end user) message log
        :param cb_cancel: Cancel callback
        :param cb_next_phase: Next phase callback
        """
        super().__init__()

        logging.debug('Initializing PhaseInputWidget')

        self.image_cache = image_cache
        self.i18n = i18n
        self.log = log
        self.cb_cancel = cb_cancel
        self.cb_next_phase = cb_next_phase

        self.widget_list = None
        self.components = []

        self.is_enabled = False

        self.setAcceptDrops(True)

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing PhaseInputWidget GUI')

        font_label_header = QFont()
        font_label_header.setBold(True)
        font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        font_label_header_small = QFont()
        font_label_header_small.setBold(False)
        font_label_header_small.setPointSize(app_conf_get('label.header.small.font.size', 18))

        font_label_info_small = QFont()
        font_label_info_small.setBold(False)
        font_label_info_small.setPointSize(app_conf_get('label.info.small.font.size', 10))

        line_css = 'background-color: #c0c0c0;'

        # Components

        label_header = QLabel(self.i18n.translate('GUI.PHASE.INPUT.HEADER'))
        label_header.setFont(font_label_header)
        label_header.setAlignment(Qt.AlignCenter)

        line_select_images_1 = QWidget()
        line_select_images_1.setFixedHeight(1)
        line_select_images_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_select_images_1.setStyleSheet(line_css)

        line_select_images_2 = QWidget()
        line_select_images_2.setFixedHeight(1)
        line_select_images_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_select_images_2.setStyleSheet(line_css)

        button_select_images = QPushButton(self.i18n.translate('GUI.PHASE.INPUT.SELECT_IMAGES'))
        button_select_images.clicked[bool].connect(self._select_images)
        self.components.append(button_select_images)

        label_dragndrop_hint = QLabel(self.i18n.translate('GUI.PHASE.INPUT.HINT'))
        label_dragndrop_hint.setFont(font_label_info_small)
        label_dragndrop_hint.setAlignment(Qt.AlignCenter)

        label_selected_images = QLabel(self.i18n.translate('GUI.PHASE.INPUT.SELECTED_IMAGES'))
        label_selected_images.setFont(font_label_header_small)
        label_selected_images.setAlignment(Qt.AlignLeft)

        label_selected_images_hint = QLabel(self.i18n.translate('GUI.PHASE.INPUT.SELECTED_IMAGES.HINT'))
        label_selected_images_hint.setFont(font_label_info_small)
        label_selected_images_hint.setAlignment(Qt.AlignLeft)

        self.widget_list = QListWidget()
        self.widget_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.widget_list.model().rowsMoved.connect(self._item_moved)
        self.widget_list.current_images = []

        button_cancel = QPushButton(self.i18n.translate('GUI.PHASE.CANCEL'))
        button_cancel.clicked[bool].connect(self._cancel)
        self.components.append(button_cancel)

        button_next_phase = QPushButton(self.i18n.translate('GUI.PHASE.INPUT.NEXT_PHASE'))
        button_next_phase.clicked[bool].connect(self._next_phase)
        self.components.append(button_next_phase)

        # Layout

        grid = QGridLayout()
        grid.setSpacing(20)

        # grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        grid.addWidget(line_select_images_1, curr_gridid, 0, 1, 4)
        grid.addWidget(label_header, curr_gridid, 4, 1, 2)
        grid.addWidget(line_select_images_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        grid.addWidget(button_select_images, curr_gridid, 0, 1, 5)
        grid.addWidget(label_dragndrop_hint, curr_gridid, 5, 1, 5)

        curr_gridid += 1
        grid.addWidget(label_selected_images, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        grid.addWidget(label_selected_images_hint, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        grid.addWidget(self.widget_list, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        grid.addWidget(button_cancel, curr_gridid, 0, 1, 4)
        grid.addWidget(button_next_phase, curr_gridid, 4, 1, 6)

        self.setLayout(grid)
        self._reset_enabled()

    def _item_moved(self, _i1, i_from, _i2, _i3, i_to):
        if len(self.widget_list.current_images) > 1:
            _imgs = self.widget_list.current_images
            elem = _imgs[i_from]
            _imgs.insert(i_to, elem)
            for i, ele in enumerate(_imgs):
                if i != i_to and ele == elem:
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

    # @override
    def dragEnterEvent(self, event):
        """dragEnterEvent

        :param event: event
        """
        if self._filter_image_files(event):
            event.accept()
        else:
            event.ignore()

    # @override
    def dropEvent(self, event):
        """dropEvent

        :param event: event
        """
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
            logging.debug('Skipping adding image "%s" since it is already contained in list', path_img)
            return
        logging.debug('Adding to list: "%s"', path_img)
        try:
            with open(path_img, encoding='utf-8') as f:
                fname = os.path.basename(f.name)
                item = QListWidgetItem(self.widget_list)
                item_widget = ListWidget(self.i18n, path_img, fname, self.widget_list)
                item.setSizeHint(item_widget.sizeHint())
                item.id = item_widget.id
                self.widget_list.addItem(item)
                self.widget_list.setItemWidget(item, item_widget)
                self.widget_list.current_images.append(path_img)
        except Exception as ex:
            logging.error('Error adding image "%s" to list: %s', path_img, ex)

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
                    logging.debug('Selected file name: "%s"', fname)
                    self._add_to_list(fname)
        else:
            self.log(self.i18n.translate('GUI.PHASE.INPUT.LOG.SELECT_IMAGES_CANCEL').format(0))
            logging.debug('Cancelled selecting files')

    def _cancel(self):
        """Cancels"""
        logging.debug('Cancel')

        if self.cb_cancel:
            self._disable()
            if not self.cb_cancel():
                self._reset_enabled()

    def _next_phase(self):
        """Goes to the next phase"""
        logging.debug('Next phase')

        err = []
        if not self.widget_list.current_images:
            err.append(self.i18n.translate('GUI.PHASE.INPUT.ERROR.NO_IMAGES_SELECTED'))
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
