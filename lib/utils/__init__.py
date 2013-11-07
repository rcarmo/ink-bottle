#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2012, Rui Carmo
Description: Utility functions
License: MIT (see LICENSE.md for details)
"""

import os, sys, logging

log = logging.getLogger()

# export commonly-used submodule symbols
from .core import Struct, Singleton, get_config, tb
from .filekit import path_for, locate
from .timekit import time_since