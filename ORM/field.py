#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LenoxWong'


class Field(object):
    # column_name, column_type, default_value, support_null, is_primary_key
    def __init__(self, name, column_type, default, not_null, primary_key):
        self.name = name
        self.column_type = column_type
        self.default = default
        self.not_null = not_null
        self.primary_key = primary_key

    def __str__(self):
        cls_name = self.__class__.__name__
        string = '<%s : %s : %s>' % (cls_name, self.name, self.column_type)
        if self.primary_key:
            string += ' (PrimaryKey)'
        return string

class IntegerField(Field):
    def __init__(self, name=None, column_type='INT', default=0, not_null=True, primary_key=False):
        super().__init__(name, column_type, default, not_null, primary_key)

class FloatField(Field):
    def __init__(self, name=None, column_type='DOUBLE', default=0.0, not_null=True, primary_key=False):
        super().__init__(name, column_type, default, not_null, primary_key)

class StringField(Field):
    def __init__(self, name=None, column_type='VARCHAR(255)', default='null', not_null=True, primary_key=False):
        super().__init__(name, column_type, default, not_null, primary_key)

class TextField(Field):
    def __init__(self, name=None, column_type='TEXT', default='null', not_null=True, primary_key=False):
        super().__init__(name, column_type, default, not_null, primary_key)

class BooleanField(Field):
    def __init__(self, name=None, column_type='BOOLEAN', default=False, not_null=True, primary_key=False):
        super().__init__(name, column_type, default, not_null, primary_key)
