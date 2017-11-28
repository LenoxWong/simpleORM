#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LenoxWong'

# for creating database
database = {
    'name': 'Test',
    'host': 'localhost',
    'user': 'test',
    'password': 'test'
},

# for creating the pool
pool = {
    'host': 'localhost',
    'port': 3306,
    'user': tuple(database)[0]['user'],
    'password': tuple(database)[0]['password'],
    'db': tuple(database)[0]['name'],
    'charset': 'utf8',
    'autocommit': True,
    'maxsize': 10,
    'minsize': 1
}
