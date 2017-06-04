import asyncio
import time

from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.util import deque
from hexi.plugin.InputPlugin import InputPlugin


EMPTY_SIGNAL = [0, 0, 0, 0, 0, 0]

class InputManager(BaseManager):
  def __init__(self):
    super().__init__('input', 'input', InputPlugin)
    self.data_log_queue = deque.WebSocketPipingDeque(maxlen=400)

  def init(self):
    super().init()

    self.last_signal = EMPTY_SIGNAL
    asyncio.ensure_future(self.fetch_signal_loop_async())

    self.data_log_queue.attach_ws_endpoint(self.bp, '/api/input_log')
    event.subscribe(self.on_input_raw_signal, ['hexi.pipeline.input.raw_data'])

  async def fetch_signal_loop_async(self):
    while True:
      signal = self.last_signal
      self.last_signal = EMPTY_SIGNAL
      self.data_log_queue.append([int(time.time()), signal])
      # TODO: test whether currently started
      asyncio.ensure_future(event.publish('hexi.pipeline.input.data', signal))
      await asyncio.sleep(1 / 20)

  async def on_input_raw_signal(self, e):
    self.last_signal = e['value']
