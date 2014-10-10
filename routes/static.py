#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Static routes

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import os, sys, logging
from bottle import route, static_file

log = logging.getLogger()


@route('/static/<path:path>')
def send_static(path):
    """Static file handler"""
    return static_file(path, root='static')

