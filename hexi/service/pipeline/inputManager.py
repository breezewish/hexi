import asyncio
import time

from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.util import deque
from hexi.plugin.InputPlugin import InputPlugin


class InputManager(BaseManager):
  def __init__(self):
    super().__init__('input', 'input', InputPlugin)
    self.data_log_queue = deque.WebSocketPipingDeque(maxlen=400)

  def init(self):
    super().init()
    self.data_log_queue.attach_ws_endpoint(self.bp, '/api/input_log')
    event.subscribe(self.on_input_raw_signal, ['hexi.pipeline.input.raw_data'])

  async def on_input_raw_signal(self, e):
    self.data_log_queue.append([int(time.time()), e['value']])
    # TODO: test whether currently started
    asyncio.ensure_future(event.publish('hexi.pipeline.input.data', e['value']))
