#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LenoxWong'


import asyncio, logging
from field import Field
from connect import SELECT, EXECUTE

# ModelMetaclass
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # just return if model name is Model
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # get the table name, if there is no attribute called '__table__' then use the model name
        table_name = attrs.get('__table__', None) or name.lower()
        logging.info("model: %s ==> table: %s" % (name, table_name))
        # find all mappings and the primary key
        mappings = {}       # all mappings
        fields = []         # except primary key
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                if v.name is None:
                    raise RuntimeError("No table column_name for model '%s' attribute '%s'" % (name, k))
                mappings[k] = v
                logging.info("find mapping: %s ==> %s" % (k, v))
                if v.primary_key is True:
                    if primary_key is not None:
                        raise RuntimeError("Duplicate primary key for model '%s'" % name)
                    primary_key = k
                else:
                    fields.append(k)
        if primary_key is None:
            raise RuntimeError("No primary key in model '%s'" % name)
        # remove mapping attributes in model
        for k, v in mappings.items():
            attrs.pop(k)
        # save mappings and table name
        attrs['__table__'] = table_name
        attrs['__mappings__'] = mappings
        attrs['__fields__'] = fields
        attrs['__primary_key__'] = primary_key
        # sql
        params = primary_key + ', ' + ', '.join(fields)
        values = []
        for i in range(len(fields) + 1):
            values.append('?')
        values = ', '.join(values)                          # ?, ?, ?...
        params_and_values = '=?, '.join(fields) + '=?'      # name=?, email=?, ...
        attrs['__select__'] = 'select * from %s' % table_name
        attrs['__insert__'] = 'insert into %s(#1) values(#2)' % table_name
        attrs['__update__'] = 'update %s set # where %s=?' % (table_name, primary_key)
        attrs['__delete__'] = 'delete from %s where %s=?' % (table_name, primary_key)

        return type.__new__(cls, name, bases, attrs)

def sql_value(v):
    if isinstance(v, str):
        return "'%s'" % v
    if isinstance(v, bool):
        return int(v)
    return v

# Model
class Model(dict, metaclass=ModelMetaclass):
    # use dict init method
    def __init__(self, **kw):
        mappings = self.__mappings__
        error_keys = []
        for k, v in kw.items():
            if k not in mappings:
                error_keys.append(k)
        # put an end to setting not mapped keys
        if len(error_keys) > 0:
            cls_name = self.__class__.__name__
            raise RuntimeError("model '%s' didn't set mapping for ( %s )" % (cls_name, ','.join(error_keys)))
        # set not_null attributes the value of default and others to None if they are not in kw
        for k, v in mappings.items():
            if k not in kw:
                if mappings[k].not_null is True:
                    kw[k] = mappings[k].default
                else:
                    kw[k] = None
        super().__init__(**kw)

    # enable and use ins.attr mehod
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise e

    def __setattr__(self, key, value):
        if key in self.__mappings__:
            self[key] = value
        else:
            raise KeyError("model '%s' has no attribute called '%s'" % (self.__class__.__name__, key))

    # classmethod
    @classmethod
    async def find(cls, **kw):
        sql = ' where '
        format_v = []
        for k, v in kw.items():
            if k not in cls.__mappings__:
                raise RuntimeError("No map for '%s' in model '%s'" % (k, cls.__name__))
            v_type = type(cls.__mappings__[k].default)
            if not isinstance(v, v_type):
                raise RuntimeError("Value type of '%s' is Wrong, '%s' needed" % (k, v_type))
            format_v.append(sql_value(v))
            sql += "%s=?, " % k
        sql = sql[:len(sql)-2]
        sql = cls.__select__ + sql
        rs = await SELECT(sql, tuple(format_v), 1)
        if len(rs) > 0:
            return cls(**rs[0])
        return None

    @classmethod
    async def findAll(cls, N=None):
        if N is None:
            rs = await SELECT(cls.__select__, ())
        elif not isinstance(N, int):
            raise RuntimeError("Integer type needed!")
        else:
            rs = await SELECT(cls.__select__, (), N)
        return list(cls(**x) for x in rs)

    @classmethod
    async def count(cls):
        sql = "select count(%s) _num_ from %s" % (cls.__primary_key__, cls.__table__)
        rs = await SELECT(sql, (), 1)
        return rs[0]['_num_']

    # instance method
    async def save(self):
        params = []
        args = []
        for k, v in self.__mappings__.items():
            value = self[k]
            if value is not None:
                params.append(k)
                args.append(sql_value(value))
        values = []
        for i in range(len(params)):
            values.append('?')
        params = ', '.join(params)
        values = ', '.join(values)
        sql = self.__insert__.replace('#1', params).replace('#2', values)
        rs = await EXECUTE(sql, tuple(args))
        logging.info("inserting success, affected rows: %s" % rs)

    async def update(self):
        params = []
        args = []
        for k, v in self.__mappings__.items():
            value = self[k]
            if value is not None:
                params.append(k)
                args.append(sql_value(value))
        args.append(sql_value(self[self.__primary_key__]))
        params_and_values = []
        for i in range(len(params)):
            params_and_values.append('%s=?' % params[i])
        params_and_values = ', '.join(params_and_values)
        sql = self.__update__.replace('#', params_and_values)
        rs = await EXECUTE(sql, tuple(args))
        logging.info("updating success, affected rows: %s" % rs)

    async def remove(self):
        logging.info("removing %s" % self)
        rs = await EXECUTE(self.__delete__, (sql_value(self[self.__primary_key__])))
        logging.info("removing success, affected rows: %s" % rs)
