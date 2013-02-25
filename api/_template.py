#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Template file for a set of API endpoints

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import os, sys, logging, json

log = logging.getLogger()

from bottle import route, get, put, post, delete, request, response, abort
import api

prefix = api.prefix + '/' #+ TODO: FILL THIS IN

# Collection URI - List
@get(prefix)
def list():
    abort(501,'Not Implemented')
    

# Collection URI - Replace entire collection
@put(prefix)
def replace():
    abort(405,'Not Allowed')


# Collection URI - Add item to collection
@post(prefix)
def append():
    abort(501,'Not Implemented')


# Collection URI - Delete entire collection
@delete(prefix)
def remove():
    abort(405,'Not Allowed')


# Element URI - Retrieve element
@get(prefix + '/<id>')
def element(id):
    abort(501,'Not Implemented')


# Element URI - Replace or create element
@put(prefix + '/<id>')
def replace(id):
    abort(501,'Not Implemented')


# Element URI - Create new named element (doesn't make sense in most cases)
@post(prefix + '/<id>')
def unused(id):
    abort(501,'Not Implemented')


# Element URI - Patch existing named element (returns 204 No content on success as per RFC 5789)
@route(prefix + '/<id>', method='PATCH')
def unused(id):
    abort(501,'Not Implemented')


# Element URI - Delete element
@delete(prefix + '/<id>')
def delete(id):
    abort(501,'Not Implemented')
