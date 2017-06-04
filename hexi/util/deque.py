import asyncio
import collections
import json


class WebSocketPipingDeque(collections.deque):

  def __init__(self, flush_interval=1, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.flush_interval = flush_interval
    self.websocket_clients = set()
    self.flush_future = asyncio.ensure_future(self.flush_async())

  def attach_ws_endpoint(self, blueprint, path):
    @blueprint.websocket(path)
    async def signal_queue_item(request, ws):
      try:
        self.pipe(ws)
        while True:
          await ws.recv()
      finally:
        self.unpipe(ws)

  async def flush_async(self):
    while True:
      for client in self.websocket_clients:
        data = json.dumps(client._backed_records)
        asyncio.ensure_future(client.send(data))
        client._backed_records = []
      await asyncio.sleep(self.flush_interval)

  def close(self):
    self.flush_future.cancel()
    for client in self.websocket_clients:
      self.unpipe(client)

  def pipe(self, ws, *, send_initial=True):
    ws._backed_records = []
    self.websocket_clients.add(ws)
    if send_initial:
      initial_data = [log for log in self]
      data = json.dumps(initial_data)
      asyncio.ensure_future(ws.send(data))

  def unpipe(self, ws):
    ws._backed_records = None
    self.websocket_clients.remove(ws)

  def append(self, data):
    super().append(data)
    for client in self.websocket_clients:
      client._backed_records.append(data)

