#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""GUI State"""

from enum import Enum, unique


@unique
class GUIState(Enum):
    """The GUI state"""
    INIT_UI = 10
    PHASE_WELCOME = 20
    PHASE_INPUT = 30
    PHASE_OUTPUT = 40
    PHASE_CONVERSION = 50
    PHASE_DONE = 60
