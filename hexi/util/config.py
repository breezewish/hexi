import functools

from hexi.service import db


def get_record_id(type, name):
  return '{0}_{1}'.format(type, name)

async def get_config(type, name, default=None):
  doc = await db.coll('config').find_one({'_id': get_record_id(type, name)})
  if doc != None:
    doc = doc['data']
  else:
    doc = default
  return doc

async def save_config(type, name, config):
  await db.coll('config').update_one(
    {'_id': get_record_id(type, name)},
    {'$set': {'data': config}},
    upsert=True)

get_core_config = functools.partial(get_config, 'core')

get_plugin_config = functools.partial(get_config, 'plugin')

save_core_config = functools.partial(save_config, 'core')

save_plugin_config = functools.partial(save_config, 'plugin')
