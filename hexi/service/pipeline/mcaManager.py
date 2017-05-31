import asyncio

from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.plugin.MCAPlugin import MCAPlugin


class MCAManager(BaseManager):
  def __init__(self):
    super().__init__('mca', 'mca', MCAPlugin)

  def init(self):
    super().init()
    event.subscribe(self.on_input_raw_signal, ['hexi.pipeline.mca.raw_data'])

  async def on_input_raw_signal(self, e):
    # currently we do nothing
    asyncio.ensure_future(event.publish('hexi.pipeline.mca.data', e['value']))
