import asyncio

from hexi.service import event

class FsxDataUdpServer:
  def connection_made(self, transport):
    self.transport = transport

  def datagram_received(self, data, addr):
    message = data.decode()
    asyncio.ensure_future(event.publish('hexi.received', message))
    #print('Received %r from %s' % (message, addr))
    #print('Send %r to %s' % (message, addr))
    #self.transport.sendto(data, addr)
