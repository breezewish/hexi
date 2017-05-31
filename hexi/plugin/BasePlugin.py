import asyncio

from yapsy.IPlugin import IPlugin
from hexi.util import config


class BasePlugin(IPlugin):
  def __init__(self):
    super().__init__()
    self.bp = None;
    self.id = None;
    self.config = {}
    self.config_default = {}
    self.category = None;
    self.configurable = False

  async def load(self):
    self.config = await config.get_plugin_config(self.id, self.config_default)

  def save_config(self):
    asyncio.ensure_future(config.save_plugin_config(self.id, self.config))
