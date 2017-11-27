#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LenoxWong'

# to approach the follow usage:
#
# # use class attributes to indicate maps and instance attributes to store the data
# class User(Model):
#     '__table__' = 'user'                                                            # table name
#     uid = IntegerField(name='uid', primary_key=True)
#     name = StringField(name='name', column_type='VARCHAR(16)')
#     email = StringField(name='email', column_type='VARCHAR(64)', not_null=False)    # email can be null
#
# user = User(uid=1, name='LenoxWong')        # instance
#
# user['name']                                # 'LenoxWong'
# user.name                                   # 'LenoxWong'
# await user.save()                           # insert the instance into table 'user'
# user.email = 'Lenox.Wong@gmail.com'
# user['email']                               # 'Lenox.Wong@gmail.com'
# user.email                                  # 'Lenox.Wong@gmail.com'
# await user.update()                         # update the instance in table 'user'
# await user.remove()                         # remove the instance in table 'user'
#
# user1 = User(uid=1, name='LenoxWong')       # ----------- user ------------
# user2 = User(uid=2, name='Others_1')        # | uid |    name     | email |
# user3 = User(uid=3, name='Others_2')        # | 1   | 'LenoxWong' |       |
# await user1.save()                          # | 2   | 'Others_1'  |       |
# await user2.save()                          # | 3   | 'Others_2'  |       |
#
# # class method
# await User.find(uid=1)                      # user1
# await User.find(name='Others_1')            # user2
# await User.find(uid=1, name='LenoxWong')    # user1
#
# await User.findAll()                        # (user1, user2, user3)
# await User.findAll(2)                       # (user1, user2)
# await User.count()                          # 3
# await user3.remove()
# await User.count()                          # 2

import asyncio, logging
from field import Field

# ModelMetaclass
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # just return if model name is Model
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # get the table name, if there is no attribute called '__table__' then use the model name
        table_name = attrs.get('__table__', None) or name
        logging.info("model: %s ==> table: %s" % (name, table_name))
        # find all mappings and the primary key
        mappings = {}       # all mappings
        fields = []         # except primary key
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                logging.info('find mapping: %s ==> %s' % (k, v))
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
        return type.__new__(cls, name, bases, attrs)

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

    @classmethod
    async def find(cls, **kw):
        pass

    @classmethod
    async def findAll(cls, n):
        pass

    @classmethod
    async def count(cls):
        pass

    # instance method
    async def save(self):
        pass

    async def update(self):
        pass

    async def remove(self):
        pass



from field import IntegerField, StringField
logging.basicConfig(level=logging.INFO)

class User(Model):
    __table__ = 'user'
    uid = IntegerField(name='uid', primary_key=True)
    name = StringField(name='name', column_type='VARCHAR(16)')
    email = StringField(name='email', column_type='VARCHAR(64)', not_null=False)

u = User(name='lenox')
print(u['uid'], u.uid, u['name'], u.name, u['email'], u.email)
u.email = 'gmail'
u.uid = 123
print(u['uid'], u.uid, u['name'], u.name, u['email'], u.email)
