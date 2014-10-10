#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main routes

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""
import os, sys, logging
from bottle import view, route

log = logging.getLogger()

@route('/')
@view('home')
def index():
    return {
        "title": "Homepage",
        "body": "Welcome to ink-bottle!"
    }

# import all other routes
import static, debug, docs
