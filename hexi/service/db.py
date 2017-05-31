import functools
import aiomongo


async def init():
  global _db
  client = await aiomongo.create_client('mongodb://localhost')
  _db = client.get_database('hexi')


@functools.lru_cache()
def coll(name):
  return aiomongo.Collection(_db, name)
