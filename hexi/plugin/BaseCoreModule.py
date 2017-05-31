import asyncio

from sanic import Blueprint
from yapsy.IPlugin import IPlugin
from hexi.util import config
from hexi.service import web

loop = asyncio.get_event_loop()


class BaseCoreModule():
  def __init__(self, id):
    self.id = id
    self.bp = Blueprint(id, url_prefix='/core/{0}'.format(id))
    self.config = {}
    self.config_default = {}

  def init(self):
    self.config = loop.run_until_complete(config.get_core_config(self.id, self.config_default))

  def register(self):
    web.app.blueprint(self.bp)

  def save_config(self):
    asyncio.ensure_future(config.save_core_config(self.id, self.config))
