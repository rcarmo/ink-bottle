#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013, Rui Carmo
Description: Database models
License: MIT (see LICENSE.md for details)
"""

import os, sys, logging, datetime
from config import settings

log = logging.getLogger()

from peewee import *

db = SqliteDatabase(settings.database_path, threadlocals=True)

class CustomModel(Model):
    """Binds the database to all our models"""

    def fields(self, fields=None, exclude=None):
        """helper for grabbing a set of fields as a dictionary"""
        model_class = type(self)
        data = {}

        fields = fields or {}
        exclude = exclude or {}
        curr_exclude = exclude.get(model_class, [])
        curr_fields = fields.get(model_class, self._meta.get_field_names())

        for field_name in curr_fields:
            if field_name in curr_exclude:
                continue
            field_obj = model_class._meta.fields[field_name]
            field_data = self._data.get(field_name)
            if isinstance(field_obj, ForeignKeyField) and field_data and field_obj.rel_model in fields:
                rel_obj = getattr(self, field_name)
                data[field_name] = rel_obj.fields(fields, exclude)
            else:
                data[field_name] = field_data
        return data

    # remember that Peewee models have an implicit integer id as primary key
    class Meta:
        database = db


class Item(CustomModel):
    """An individual item of some kind"""
    guid    = CharField()
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
            (('created',), False),
            (('guid',), True),
        )
        order_by = ('-created',)


def setup(skip_if_existing = True):
    """Create tables for all models"""
    models = [Item]

    for item in models:
        item.create_table(skip_if_existing)
    # set Write Ahead Log mode for SQLite
    db.execute_sql('PRAGMA journal_mode=WAL')
    
    
if __name__ == '__main__':
    setup()
