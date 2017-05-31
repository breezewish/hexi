import asyncio

from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.plugin.InputPlugin import InputPlugin


class InputManager(BaseManager):
  def __init__(self):
    super().__init__('input', 'input', InputPlugin)

  def init(self):
    super().init()
    event.subscribe(self.on_input_raw_signal, ['hexi.pipeline.input.raw_data'])

  async def on_input_raw_signal(self, e):
    # TODO: test whether currently started
    asyncio.ensure_future(event.publish('hexi.pipeline.input.data', e['value']))
