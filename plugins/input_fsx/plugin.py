import time
import asyncio
import ipaddress
import logging
import numpy
import scipy.constants

from sanic import response
from hexi.util import deque
from hexi.plugin.InputPlugin import InputPlugin
from plugins.input_fsx import DataChannel

_logger = logging.getLogger(__name__)


class PluginInputFsx(InputPlugin):

  CHANNEL_UDP_PORT = 16314
  CHANNEL_TCP_PORT = 16315
  CHANNEL_UDP_PORT_TEST = 16316

  def __init__(self):
    super().__init__()
    self.configurable = True
    self.config_default = {
      'udp_port': PluginInputFsx.CHANNEL_UDP_PORT,
      'tcp_host': None,
      'tcp_port': PluginInputFsx.CHANNEL_TCP_PORT,
    }
    self.channel = None
    self.udp_analytics_log_queue = deque.WebSocketPipingDeque(maxlen=100)

  def load(self):
    super().load()

    @self.bp.route('/api/config', methods=['GET'])
    async def get_config(request):
      return response.json({ 'code': 200, 'data': self.config })

    @self.bp.route('/api/config', methods=['POST'])
    async def set_config(request):
      try:
        self.set_config(request.json)
        return response.json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return response.json({ 'code': 400, 'reason': str(e) })

    self.udp_analytics_log_queue.attach_ws_endpoint(self.bp, '/api/udp_log')

  def activate(self):
    super().activate()
    self.try_create_channel()

  def deactivate(self):
    self.try_destroy_channel()
    super().deactivate()

  def set_config(self, config):
    self.config['udp_port'] = int(config['udp_port'])
    self.config['tcp_host'] = ipaddress.ip_address(config['tcp_host']).exploded
    self.config['tcp_port'] = int(config['tcp_port'])
    self.save_config()
    self.try_create_channel()

  def try_create_channel(self):
    if self.channel != None:
      return
    if not self.is_activated:
      return
    if self.config['tcp_host'] == None or self.config['tcp_port'] == None:
      return
    self.channel = DataChannel.DataChannel(
      self.config['udp_port'],
      self.config['tcp_host'],
      self.config['tcp_port'])
    self.channel.ee.on('udp_received_message', self.on_udp_received_message)
    self.channel.ee.on('udp_analytics_tick', self.on_udp_analytics_tick)
    self.start_future = asyncio.ensure_future(self.channel.start_async())
    self.start_future.add_done_callback(self.on_start_done)

  def on_start_done(self, future):
    self.start_future = None

  def try_destroy_channel(self):
    if self.channel == None:
      return
    if self.start_future != None:
      self.start_future.cancel()
    self.channel.stop()
    self.channel = None

  def on_udp_analytics_tick(self, data):
    self.udp_analytics_log_queue.append([
      int(time.time()),
      data['receive_tick'],
      data['discard_tick']
    ])

  def on_udp_received_message(self, msg):
    self.emit_input_signal([
      # convert foot to meter
      scipy.constants.foot * msg.transmissionDataBody.zAcceleration,   # forward/backward
      scipy.constants.foot * msg.transmissionDataBody.xAcceleration,   # left/right
      scipy.constants.foot * msg.transmissionDataBody.yAcceleration,   # up/down
      # convert degree to radians
      numpy.deg2rad(msg.transmissionDataBody.rollVelocity),
      numpy.deg2rad(msg.transmissionDataBody.pitchVelocity),
      numpy.deg2rad(msg.transmissionDataBody.yawVelocity)])

