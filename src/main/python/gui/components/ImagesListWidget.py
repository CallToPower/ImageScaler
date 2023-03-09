#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Images list widget"""

from PyQt5.QtGui import QListWidget

class ImagesList(QListWidget):

    def Clicked(self,item):
        QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())
