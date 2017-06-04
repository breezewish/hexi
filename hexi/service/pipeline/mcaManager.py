import asyncio
import time

from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.util import deque
from hexi.plugin.MCAPlugin import MCAPlugin


class MCAManager(BaseManager):
  def __init__(self):
    super().__init__('mca', 'mca', MCAPlugin)
    self.data_log_queue = deque.WebSocketPipingDeque(maxlen=400)

  def init(self):
    super().init()
    self.data_log_queue.attach_ws_endpoint(self.bp, '/api/mca_log')
    event.subscribe(self.on_mca_raw_signal, ['hexi.pipeline.mca.raw_data'])

  async def on_mca_raw_signal(self, e):
    input_signal, mca_signal = e['value']
    self.data_log_queue.append([int(time.time()), mca_signal])
    asyncio.ensure_future(event.publish('hexi.pipeline.mca.data', e['value']))
