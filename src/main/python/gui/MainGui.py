#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2020 Denis Meyer
#
# This file is part of ImageScaler.
#

"""GUI"""

import logging
import sys

from gui.components.AppContext import AppContext


class GUI():
    """Main GUI"""

    def __init__(self):
        """Initializes the GUI"""
        logging.debug('Initializing MainGUI')

        appctxt = AppContext()
        exit_code = appctxt.run()
        sys.exit(exit_code)
