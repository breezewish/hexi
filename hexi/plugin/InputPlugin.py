import asyncio

from hexi.plugin.BasePlugin import BasePlugin
from hexi.service import event


class InputPlugin(BasePlugin):
  def emit_input_signal(self, data):
    """
      data should be [x, y, z, alpha, beta, gamma]
    """
    asyncio.ensure_future(event.publish('hexi.pipeline.input.raw_data', data))
