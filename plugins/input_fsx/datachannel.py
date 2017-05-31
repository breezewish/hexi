import time
import asyncio
import random
import pyee
import logging

from plugins.input_fsx import fsx_pb2
from hexi.service import event


_logger = logging.getLogger(__name__)


class UDPServer(asyncio.DatagramProtocol):

  SERIAL_COUNTER_MAX = 0x2FFFFFFF

  def __init__(self, manager, token):
    super().__init__()
    self.manager = manager
    self.token = token
    self.sn = 0

  def datagram_received(self, data, addr):
    try:
      # Note: there are no length prefix in UDP packets
      msg = fsx_pb2.UdpResponseMessage()
      msg.ParseFromString(data)
      if msg.token != self.token:
        _logger.warn('A message is discarded because of incorrect token')
        print(msg.token, self.token)
        self.manager.ee.emit('udp_discarded_message')
        return
      if msg.serialNumber + UDPServer.SERIAL_COUNTER_MAX <= self.sn + UDPServer.SERIAL_COUNTER_MAX:
        _logger.warn('A message is discarded because of received newer message')
        self.manager.ee.emit('udp_discarded_message')
        return
      self.sn = msg.serialNumber
      self.manager.ee.emit('udp_received_message', msg)
    except Exception as e:
      _logger.warn(e)
      self.manager.ee.emit('udp_discarded_message')

  def connection_lost(self, exc):
    self.manager.ee.emit('udp_closed')


class TCPClientManager(object):
  def __init__(self, channel, host, port, retry_sec=2):
    self.channel = channel
    self.host = host
    self.port = port
    self.retry_sec = retry_sec
    self.work_future = None
    self.connect_future = None
    self.reconnect_future = None
    self.reader = None
    self.writer = None
    self.state = 'idle'
    self.ee = channel.ee

  async def connect_async(self):
    while True and (self.state in ['connecting', 'reconnecting']):
      try:
        future = asyncio.open_connection(self.host, self.port)
        reader, writer = await asyncio.wait_for(future, timeout=3)
        _logger.debug('Telemetry connected')
        self.reader = reader
        self.writer = writer
        self.state = 'connected'
        self.work_future = asyncio.ensure_future(self.work_async())
        self.work_future.add_done_callback(self.on_work_done)
        self.heartbeat_future = asyncio.ensure_future(self.heartbeat_async())
        self.heartbeat_future.add_done_callback(self.on_heartbeat_done)
        self.ee.emit('tcp_connected')
        break
      except (OSError, asyncio.TimeoutError):
        #print('Server not connected, retry in {0} seconds'.format(self.retry_sec))
        await asyncio.sleep(self.retry_sec)

  def connect(self):
    assert(self.state in ['idle', 'disconnected'])
    assert(self.connect_future == None)
    self.state = 'connecting'
    self.connect_future = asyncio.ensure_future(self.connect_async())
    self.connect_future.add_done_callback(self.on_connect_done)
    return self.connect_future

  def on_connect_done(self, future):
    self.connect_future = None

  async def heartbeat_async(self):
    while True:
      await asyncio.sleep(10)
      msg = fsx_pb2.TcpRequestMessage()
      msg.msgType = fsx_pb2.TcpRequestMessage.MSG_TYPE_PING
      msg.pingBody.timeStamp = int(time.time())
      self.write_message(msg)

  def on_heartbeat_done(self, future):
    self.heartbeat_future = None

  async def work_async(self):
    try:
      while True:
        size_buffer = await self.reader.readexactly(4)
        size = int.from_bytes(size_buffer, byteorder='little')
        body_buffer = await self.reader.readexactly(size)
        msg = fsx_pb2.TcpResponseMessage()
        msg.ParseFromString(body_buffer)
        self.ee.emit('tcp_received_message', msg)
    except (asyncio.IncompleteReadError, ConnectionResetError, ConnectionAbortedError):
      pass

  def on_work_done(self, future):
    _logger.debug('Telemetry connection lost')
    self.work_future = None
    if self.heartbeat_future != None:
      self.heartbeat_future.cancel()
    self.reader = None
    self.writer = None
    if self.state != 'disconnected':
      self.reconnect()

  async def reconnect_async(self):
    await self.connect_async()

  def reconnect(self):
    assert(self.state == 'connected')
    assert(self.reconnect_future == None)
    _logger.debug('Telemetry reconnecting')
    self.state = 'reconnecting'
    self.reconnect_future = asyncio.ensure_future(self.reconnect_async())
    self.reconnect_future.add_done_callback(self.on_reconnect_done)
    return self.reconnect_future

  def on_reconnect_done(self, f):
    self.reconnect_future = None

  def disconnect(self):
    assert(self.state in ['connecting', 'connected', 'reconnecting'])
    self.state = 'disconnected'
    if self.connect_future != None:
      self.connect_future.cancel()
    if self.reconnect_future != None:
      self.reconnect_future.cancel()
    if self.work_future != None:
      self.work_future.cancel()
    if self.heartbeat_future != None:
      self.heartbeat_future.cancel()
    if self.writer != None:
      self.writer.close()

  def write_message(self, msg):
    data = msg.SerializeToString()
    data = len(data).to_bytes(4, byteorder = 'little') + data
    self.writer.write(data)

class UDPServerManager(object):
  def __init__(self, channel, token, host, port):
    self.channel = channel
    self.token = token
    self.host = host
    self.port = port
    self.transport = None
    self.protocol = None
    self.state = 'idle'
    self.ee = channel.ee

  def protocol_factory(self):
    return UDPServer(self, self.token)

  async def create_endpoint_async(self):
    assert(self.state in ['idle', 'closed'])
    self.state = 'opening'
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
      self.protocol_factory, local_addr=(self.host, self.port))
    self.transport = transport
    self.protocol = protocol
    self.state = 'opened'
    _logger.debug('Telemetry receiver listening at {0}:{1}'.format(self.host, self.port))

  def close(self):
    assert(self.state in ['opening', 'opened'])
    _logger.debug('Telemetry receiver is closing')
    self.state = 'closed'
    if self.transport != None:
      self.transport.close()
      self.transport == None
      self.protocol == None


class DataChannel(object):
  def __init__(self, udp_port, tcp_host, tcp_port):
    self.ee = pyee.EventEmitter()
    self.udp_token = random.randint(0, 0x6FFFFFFF)
    self.tcp = TCPClientManager(self, tcp_host, tcp_port)
    self.udp = UDPServerManager(self, self.udp_token, '0.0.0.0', udp_port)
    self.udp_receive_counter = 0
    self.udp_discard_counter = 0
    self.ee.on('tcp_connected', self.on_tcp_connected)
    self.ee.on('tcp_received_message', self.on_tcp_received_message)
    self.ee.on('udp_received_message', self.on_udp_received_message)
    self.ee.on('udp_discarded_message', self.on_udp_discarded_message)

  async def udp_analytics_async(self):
    last_receive = 0
    last_discard = 0
    while True:
      await asyncio.sleep(1)
      delta_receive = self.udp_receive_counter - last_receive
      delta_discard = self.udp_discard_counter - last_discard
      last_receive = self.udp_receive_counter
      last_discard = self.udp_discard_counter
      self.ee.emit('udp_analytics_tick', {
        'receive_all': last_receive,
        'discard_all': last_discard,
        'receive_tick': delta_receive,
        'discard_tick': delta_discard})

  def on_udp_analytics_done(self, future):
    self.udp_analytics_future = None

  async def start_async(self):
    _logger.debug('Starting telemetry channel')
    self.udp_analytics_future = asyncio.ensure_future(self.udp_analytics_async())
    self.udp_analytics_future.add_done_callback(self.on_udp_analytics_done)
    await self.udp.create_endpoint_async()
    await self.tcp.connect()
    _logger.debug('Telemetry channel started')

  def stop(self):
    _logger.debug('Stopping telemetry channel')
    if self.udp_analytics_future != None:
      self.udp_analytics_future.cancel()
    self.tcp.disconnect()
    self.udp.close()

  def on_tcp_connected(self):
    self.udp.protocol.sn = 0
    msg = fsx_pb2.TcpRequestMessage()
    msg.msgType = fsx_pb2.TcpRequestMessage.MSG_TYPE_SET_CONFIG
    msg.setConfigBody.udpPort = 4900
    msg.setConfigBody.udpToken = channel.udp_token
    self.tcp.write_message(msg)

  def on_tcp_received_message(self, msg):
    if msg.success != True:
      _logger.error('Telemetry command failed')

  def on_udp_received_message(self, msg):
    self.udp_receive_counter = self.udp_receive_counter + 1

  def on_udp_discarded_message(self):
    self.udp_discard_counter = self.udp_discard_counter + 1
