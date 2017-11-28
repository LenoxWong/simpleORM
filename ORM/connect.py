#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LenoxWong'


import asyncio, logging
import aiomysql

# import asyncio
# import configs
# from connect import CREATE_POOL
# loop = asyncio.get_event_loop()
# CREATE_POOL(loop, **configs.pool)
async def CREATE_POOL(loop, **kw):
    logging.info("creating database connection pool...")
    global __pool
    __pool = await aiomysql.create_pool(loop=loop, **kw)
    logging.info("connection pool created")

async def DESTROY_POOL():
    global __pool
    if __pool is not None:
        logging.info("closing the connection pool...")
        __pool.close()
        await __pool.wait_closed()
        logging.info("connection pool closed")

# sql: =? where a=? ...
# args: (a, b, c...)
def complete_sql(sql, args):
    sql = sql.replace('?', '%s')
    sql = sql % args
    logging.info("sql: %s" % sql )
    return sql + ';'

async def SELECT(sql, args, size=None):
    sql = complete_sql(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            if size is None:
                rs = cur.fetchall()
            else:
                rs = cur.fetchmany(size)
        rs = rs.result()
        logging.info("row returned %s" % len(rs))
        return rs

async def EXECUTE(sql, args):
    sql = complete_sql(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            affected = cur.rowcount
        return affected
