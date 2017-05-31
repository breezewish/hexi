import asyncio
import ipaddress
import collections
import logging

from sanic.response import json
from hexi.plugin.InputPlugin import InputPlugin
from hexi.service import event
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
    #self.udp_analytics_log_queue = collections.deque(maxlen=500)
    #self.udp_data_log_queue = collections.deque(maxlen=500)

  def load(self):
    super().load()

    @self.bp.route('/api/config', methods=['GET'])
    async def webGetConfig(request):
      return json({ 'code': 200, 'data': self.config })

    @self.bp.route('/api/config', methods=['POST'])
    async def webSetConfig(request):
      try:
        self.set_config(request.json)
        return json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return json({ 'code': 400, 'reason': str(e) })

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

  def on_udp_received_message(self, msg):
    # !! cood-system is different between Hexi's and Fsx's
    event.publish('hexi.pipeline.input.data', {
      'x': msg.transmissionDataBody.zAcceleration,  # forward/backward
      'y': msg.transmissionDataBody.xAcceleration,  # left/right
      'z': msg.transmissionDataBody.yAcceleration,  # up/down
      'alpha': msg.transmissionDataBody.rollVelocity,
      'beta': msg.transmissionDataBody.pitchVelocity,
      'gamma': msg.transmissionDataBody.yawVelocity})
