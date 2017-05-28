import signal
import time


import asyncio
import random
import pyee

from plugins.input_fsx import fsx_pb2


class UDPServer(asyncio.DatagramProtocol):
  def __init__(self, manager):
    super().__init__()
    self.manager = manager

  def datagram_received(self, data, addr):
    self.manager.ee.emit('udp_received', data, addr)

  def connection_lost(self, exc):
    self.manager.ee.emit('udp_closed')


class TCPClient(asyncio.Protocol):
  def __init__(self, manager):
    super().__init__()
    self.manager = manager

  def connection_lost(self, exc):
    self.manager.ee.emit('tcp_disconnected')


class TCPClientManager(object):
  def __init__(self, channel, host, port, retry_sec=2):
    self.channel = channel
    self.host = host
    self.port = port
    self.retry_sec = retry_sec
    self.connect_future = None
    self.reconnect_future = None
    self.transport = None
    self.protocol = None
    self.state = 'idle'
    self.ee = channel.ee
    self.ee.on('tcp_disconnected', self.on_tcp_disconnected)

  def protocol_factory(self):
    return TCPClient(self)

  async def connect_async(self):
    while True and (self.state in ['connecting', 'reconnecting']):
      try:
        transport, protocol = await loop.create_connection(
          self.protocol_factory, self.host, self.port)
        print('tcp connected')
        self.transport = transport
        self.protocol = protocol
        self.state = 'connected'
        self.ee.emit('tcp_connected', transport)
        break
      except OSError:
        print('Server not connected, retry in {0} seconds'.format(self.retry_sec))
        await asyncio.sleep(self.retry_sec)

  def connect(self):
    assert(self.state in ['idle', 'disconnected'])
    assert(self.connect_future == None)
    print('tcp connecting')
    self.state = 'connecting'
    self.connect_future = asyncio.ensure_future(self.connect_async())
    self.connect_future.add_done_callback(self.on_connect_done)
    return self.connect_future

  def on_connect_done(self, future):
    self.connect_future = None

  def on_tcp_disconnected(self):
    print('tcp connection lost')
    self.transport = None
    self.protocol = None
    if self.state != 'disconnected':
      self.reconnect()

  async def reconnect_async(self):
    await self.connect_async()

  def reconnect(self):
    assert(self.state == 'connected')
    assert(self.reconnect_future == None)
    print('tcp reconnecting...')
    self.state = 'reconnecting'
    self.reconnect_future = asyncio.ensure_future(self.reconnect_async())
    self.reconnect_future.add_done_callback(self.on_reconnect_done)
    return self.reconnect_future

  def on_reconnect_done(self, f):
    print('tcp reconnected')
    self.reconnect_future = None

  def disconnect(self):
    assert(self.state in ['connecting', 'connected', 'reconnecting'])
    print('called tcp disconnect')
    self.state = 'disconnected'
    if self.connect_future != None:
      self.connect_future.cancel()
    if self.reconnect_future != None:
      self.reconnect_future.cancel()
    if self.transport != None:
      self.transport.close()


class UDPServerManager(object):
  def __init__(self, channel, host, port):
    self.channel = channel
    self.host = host
    self.port = port
    self.transport = None
    self.protocol = None
    self.state = 'idle'
    self.ee = channel.ee

  def protocol_factory(self):
    return UDPServer(self)

  async def create_endpoint_async(self):
    assert(self.state in ['idle', 'closed'])
    print('creating udp server')
    self.state = 'opening'
    transport, protocol = await loop.create_datagram_endpoint(
      self.protocol_factory, local_addr=(self.host, self.port))
    self.transport = transport
    self.protocol = protocol
    self.state = 'opened'
    print('udp server created')

  def close(self):
    assert(self.state in ['opening', 'opened'])
    print('called udp server close')
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
    self.udp = UDPServerManager(self, '0.0.0.0', udp_port)
    #self.ee.on('tcp_connected', self.on_tcp_connected)
    #self.ee.on('udp_received', self.on_udp_received)

  async def start_async(self):
    print('data channel start')
    await self.udp.create_endpoint_async()
    await self.tcp.connect()
    print('data channel started')

  def stop(self):
    print('data channel stop')
    self.tcp.disconnect()
    self.udp.close()

  #def on_tcp_connected(self):
  #  pass

  #def on_udp_received(self, data, addr):
  #  if self.tcp.state != 'connected':
  #    print('udp packet ignored because tcp is not connected')
  #    return
  #  pass


channel = DataChannel(4900, '127.0.0.1', 4905)

@channel.ee.on('tcp_connected')
def tcp_connected(transport):
  msg = fsx_pb2.TcpRequestMessage()
  msg.msgType = fsx_pb2.TcpRequestMessage.MSG_TYPE_SET_CONFIG
  msg.setConfigBody.udpPort = 4900
  msg.setConfigBody.udpToken = channel.udp_token
  msg.setConfigBody.updateFreq = 10
  data = msg.SerializeToString()
  transport.write(data)


asyncio.ensure_future(channel.start_async())

loop = asyncio.get_event_loop()
def handleSignal1():
  print('emulate stop')
  channel.stop()

loop.add_signal_handler(signal.SIGUSR1, handleSignal1)

def handleSignal2():
  print('emulate start')
  asyncio.ensure_future(channel.start_async())

loop.add_signal_handler(signal.SIGUSR2, handleSignal2)

try:
  loop.run_forever()
except KeyboardInterrupt as e:
  #channel.stop()
  loop.stop()

"""
def handleSigInt(s, e):
  channel.stop()
  loop.stop()

signal.signal(signal.SIGINT, handleSigInt)

channel.start()
try:
  loop.run_forever()
except asyncio.CancelledError:
  print('CancelledError')

loop.close()
"""
