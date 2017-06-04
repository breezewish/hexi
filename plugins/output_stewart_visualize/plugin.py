import json
import asyncio
import logging
import numpy

from sanic import response
from hexi.plugin.OutputPlugin import OutputPlugin

_logger = logging.getLogger(__name__)


class PluginOutputStewartVisualize(OutputPlugin):

  def __init__(self):
    super().__init__()
    self.configurable = True
    self.connected_clients = set()

  def handle_motion_signal(self, input_signal, motion_signal):
    data_to_send = json.dumps(motion_signal)
    for client in self.connected_clients:
      asyncio.ensure_future(client.send(data_to_send))

  def load(self):
    super().load()

    @self.bp.websocket('/api/signal')
    async def signal_feed(request, ws):
      try:
        self.connected_clients.add(ws)
        while True:
          await ws.recv()
      finally:
        self.connected_clients.remove(ws)
