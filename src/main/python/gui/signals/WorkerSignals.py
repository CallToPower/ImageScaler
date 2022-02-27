#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Worker Signals"""

from PyQt5.QtCore import QObject, pyqtSignal


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    scalingerror
        `object` error data, anything
    scalingresult
        `object` data returned from processing, anything
        - [0] Number of scaled images
        - [1] Number of images to be processed
    scalingfinished
        `object` data returned from processing, anything
        - [0] Number of scaled images
        - [1] Number of images to be processed
    """
    scalingerror = pyqtSignal(object)
    scalingresult = pyqtSignal(object, object)
    scalingfinished = pyqtSignal(object, object)
