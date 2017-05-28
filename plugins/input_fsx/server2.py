import signal


import asyncio
import random


class UDPServer(asyncio.DatagramProtocol):
  def __init__(self):
    super().__init__()
    self.manager = None

  def set_manager_instance(self, manager):
    assert(self.manager == None)
    self.manager = manager

  def connection_made(self, transport):
    self.transport = transport

  def datagram_received(self, data, addr):
    self.manager.on_datagram_received(data, addr)
    #message = data.decode()
    #print('message received: {0}'.format(message))

  def connection_lost(self, exc):
    print('udp connection lost')
    assert(self.manager != None)
    self.manager = None


class TCPClient(asyncio.Protocol):
  def __init__(self):
    super().__init__()
    self.manager = None

  def set_manager_instance(self, manager):
    assert(self.manager == None)
    self.manager = manager

  def connection_made(self, transport):
    self.transport = transport
    self.manager.on_connection_made()

  def connection_lost(self, exc):
    assert(self.manager != None)
    self.manager.on_connection_lost()
    self.manager = None


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

  async def connect_async(self):
    while True and (self.state in ['connecting', 'reconnecting']):
      try:
        transport, protocol = await loop.create_connection(
          TCPClient, self.host, self.port)
        self.transport = transport
        self.protocol = protocol
        self.protocol.set_manager_instance(self)
        self.state = 'connected'
        print('tcp connected')
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

  def on_connection_lost(self):
    print('tcp connection lost')
    self.transport = None
    self.protocol = None
    if self.state != 'disconnected':
      self.reconnect()

  def on_connection_made(self):
    self.channel.on_tcp_connection_made()

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

  async def create_endpoint_async(self):
    assert(self.state in ['idle', 'closed'])
    print('creating udp server')
    self.state = 'opening'
    transport, protocol = await loop.create_datagram_endpoint(UDPServer, local_addr=(self.host, self.port))
    self.transport = transport
    self.protocol = protocol
    self.protocol.set_manager_instance(self)
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

  def on_datagram_received(self, data, addr):
    self.channel.on_udp_received(data, addr)


class DataChannel(object):
  def __init__(self, udp_port, tcp_host, tcp_port):
    self.udp_token = random.randint(0, 0x6FFFFFFF)
    self.tcp = TCPClientManager(self, tcp_host, tcp_port)
    self.udp = UDPServerManager(self, '0.0.0.0', udp_port)

  async def start_async(self):
    print('data channel start')
    await self.udp.create_endpoint_async()
    await self.tcp.connect()
    print('data channel started')

  def stop(self):
    print('data channel stop')
    self.tcp.disconnect()
    self.udp.close()

  def on_tcp_connection_made(self):
    pass

  def on_udp_received(self, data, addr):
    if self.tcp.state != 'connected':
      print('udp packet ignored because tcp is not connected')
      return
    pass


channel = DataChannel(4900, '127.0.0.1', 4905)
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
