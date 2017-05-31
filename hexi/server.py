import logging
import logging.config
import sys
import asyncio
import uvloop
import signal
import sanic.config

from hexi.util import taillog

_logger = logging.getLogger(__name__)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
signal.signal(signal.SIGINT, lambda s, f: loop.stop())


def load_core_module(BaseClass):
  module = BaseClass()
  module.init()
  module.register()


def main():
  sanic.config.LOGGING['handlers']['memoryTailLog'] = {
    '()': taillog.TailLogHandler,
    'log_queue': taillog.log_queue,
    'filters': ['accessFilter'],
    'formatter': 'simple',
  }
  sanic.config.LOGGING['root'] = {
    'level': 'DEBUG',
    'handlers': ['internal', 'errorStream', 'memoryTailLog'],
  }
  sanic.config.LOGGING['loggers']['sanic']['propagate'] = False
  sanic.config.LOGGING['loggers']['sanic']['handlers'].append('memoryTailLog')
  sanic.config.LOGGING['loggers']['network']['propagate'] = False
  sanic.config.LOGGING['loggers']['network']['handlers'].append('memoryTailLog')
  sanic.config.LOGGING['disable_existing_loggers'] = False
  logging.config.dictConfig(sanic.config.LOGGING)

  _logger.info('Loading base modules...')
  from hexi.service import event
  from hexi.service import db
  from hexi.service import plugin
  from hexi.service import web
  from hexi.service import log
  loop.run_until_complete(db.init())
  plugin.init()
  web.init()
  log.init()

  _logger.info('Loading base plugins...')
  from hexi.service.pipeline import InputManager
  from hexi.service.pipeline import mcaManager
  from hexi.service.pipeline import outputManager
  load_core_module(InputManager.InputManager)
  mcaManager.init()
  outputManager.init()

  _logger.info('Loading external modules...')
  plugin.load()

  _logger.info('Starting...')
  loop.run_until_complete(event.publish('hexi.start', None))
  loop.run_forever()
  loop.run_until_complete(event.publish('hexi.stop', None))

if __name__ == '__main__':
  main()
