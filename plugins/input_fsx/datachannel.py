import asyncio

from hexi.service import event

class UDPServer(object):
  def connection_made(self, transport):
    self.transport = transport

  def datagram_received(self, data, addr):
    message = data.decode()
    asyncio.ensure_future(event.publish('hexi.received', message))
    #print('Received %r from %s' % (message, addr))
    #print('Send %r to %s' % (message, addr))
    #self.transport.sendto(data, addr)


class DataChannel(object):
  def __init__(self, udp_port, tcp_port):
    self.udp_server = loop.create_datagram_endpoint(UDPServer, local_addr=(addr, udp_port))
    asyncio.ensure_future(udp_server)
