
import asyncio, logging;logging.basicConfig(level=logging.INFO)

from model import Model
from field import IntegerField, StringField
from connect import CREATE_POOL, DESTROY_POOL
import configs

class User(Model):
    __table__ = 'users'
    uid = IntegerField(name='uid', primary_key=True)
    name = StringField(name='name', column_type='VARCHAR(16)')
    email = StringField(name='email', column_type='VARCHAR(64)', not_null=False)

user = User(uid=0, name='LenoxWong', email='Lenox.Wong@gmail.com')
other1 = User(uid=1, name='Other1', email=None)
other2 = User(uid=2, name='Other2', email=None)
other3 = User(uid=3, name='Other3', email=None)

async def test_save():
    logging.info("-------------------- test_save --------------------")
    await user.save()
    await other1.save()
    await other2.save()
    await other3.save()
    rs = await User.find(uid=0)
    logging.info('user saved: %s' % user)
    logging.info('user found: %s' % rs)

async def test_update():
    logging.info("------------------- test_update --------------------")
    user.name='Not LenoxWong'
    await user.update()
    rs = await User.find(uid=0)
    logging.info('user updated: %s' % user)
    logging.info('user found: %s' % rs)

async def test_remove():
    logging.info("------------------- test_remove --------------------")
    await user.remove()
    rs = await User.find()
    logging.info('user removed: %s' % user)
    logging.info('user found: %s' % rs)

async def test_find():
    logging.info("-------------------- test_find ---------------------")
    rs = await User.find(uid=1)
    logging.info('users found: %s' % rs)

async def test_findAll():
    logging.info("------------------- test_findAll -------------------")
    rs = await User.findAll()
    logging.info('users found: %s' % rs)
    rs = await User.findAll(2)
    logging.info('users found: %s' % rs)

async def test_count():
    logging.info("-------------------- test_count ---------------------")
    rs = await User.count()
    logging.info('users found: %s' % rs)
    await other3.remove()
    rs = await User.count()
    logging.info('users found: %s' % rs)

async def test(loop):
    logging.info("---------------------- test ------------------------")
    await CREATE_POOL(loop, **configs.pool)
    await test_save()
    await test_update()
    await test_remove()
    await test_find()
    await test_findAll()
    await test_count()
    logging.info("--------------------close pool-----------------------")
    await DESTROY_POOL()
    logging.info("-----------------------------------------------------")


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()

# INFO:root:model: User ==> table: users
# INFO:root:find mapping: uid ==> <IntegerField : uid : INT> (PrimaryKey)
# INFO:root:find mapping: name ==> <StringField : name : VARCHAR(16)>
# INFO:root:find mapping: email ==> <StringField : email : VARCHAR(64)>
# INFO:root:---------------------- test ------------------------
# INFO:root:creating database connection pool...
# INFO:root:connection pool created
# INFO:root:-------------------- test_save --------------------
# INFO:root:sql: insert into users(uid, name, email) values(0, 'LenoxWong', 'Lenox.Wong@gmail.com')
# INFO:root:inserting success, affected rows: 1
# INFO:root:sql: insert into users(uid, name) values(1, 'Other1')
# INFO:root:inserting success, affected rows: 1
# INFO:root:sql: insert into users(uid, name) values(2, 'Other2')
# INFO:root:inserting success, affected rows: 1
# INFO:root:sql: insert into users(uid, name) values(3, 'Other3')
# INFO:root:inserting success, affected rows: 1
# INFO:root:sql: select * from users where uid=0
# INFO:root:row returned 1
# INFO:root:user saved: {'uid': 0, 'name': 'LenoxWong', 'email': 'Lenox.Wong@gmail.com'}
# INFO:root:user found: {'uid': 0, 'name': 'LenoxWong', 'email': 'Lenox.Wong@gmail.com'}
# INFO:root:------------------- test_update --------------------
# INFO:root:sql: update users set uid=0, name='Not LenoxWong', email='Lenox.Wong@gmail.com' where uid=0
# INFO:root:updating success, affected rows: 1
# INFO:root:sql: select * from users where uid=0
# INFO:root:row returned 1
# INFO:root:user updated: {'uid': 0, 'name': 'Not LenoxWong', 'email': 'Lenox.Wong@gmail.com'}
# INFO:root:user found: {'uid': 0, 'name': 'Not LenoxWong', 'email': 'Lenox.Wong@gmail.com'}
# INFO:root:------------------- test_remove --------------------
# INFO:root:removing {'uid': 0, 'name': 'Not LenoxWong', 'email': 'Lenox.Wong@gmail.com'}
# INFO:root:sql: delete from users where uid=0
# INFO:root:removing success, affected rows: 1
# INFO:root:sql: select * from users wher
# INFO:root:row returned 1
# INFO:root:user removed: {'uid': 0, 'name': 'Not LenoxWong', 'email': 'Lenox.Wong@gmail.com'}
# INFO:root:user found: {'uid': 1, 'name': 'Other1', 'email': None}
# INFO:root:-------------------- test_find ---------------------
# INFO:root:sql: select * from users where uid=1
# INFO:root:row returned 1
# INFO:root:users found: {'uid': 1, 'name': 'Other1', 'email': None}
# INFO:root:------------------- test_findAll -------------------
# INFO:root:sql: select * from users
# INFO:root:row returned 3
# INFO:root:users found: [{'uid': 1, 'name': 'Other1', 'email': None}, {'uid': 2, 'name': 'Other2', 'email': None}, {'uid': 3, 'name': 'Other3', 'email': None}]
# INFO:root:sql: select * from users
# INFO:root:row returned 2
# INFO:root:users found: [{'uid': 1, 'name': 'Other1', 'email': None}, {'uid': 2, 'name': 'Other2', 'email': None}]
# INFO:root:-------------------- test_count ---------------------
# INFO:root:sql: select count(uid) _num_ from users
# INFO:root:row returned 1
# INFO:root:users found: 3
# INFO:root:removing {'uid': 3, 'name': 'Other3', 'email': None}
# INFO:root:sql: delete from users where uid=3
# INFO:root:removing success, affected rows: 1
# INFO:root:sql: select count(uid) _num_ from users
# INFO:root:row returned 1
# INFO:root:users found: 2
# INFO:root:--------------------close pool-----------------------
# INFO:root:closing the connection pool...
# INFO:root:connection pool closed
# INFO:root:-----------------------------------------------------
