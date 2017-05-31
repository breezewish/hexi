import functools

import motor.motor_asyncio


def init():
  global _db
  client = motor.motor_asyncio.AsyncIOMotorClient()
  _db = client['hexi']


@functools.lru_cache()
def coll(name):
  return _db[name]
