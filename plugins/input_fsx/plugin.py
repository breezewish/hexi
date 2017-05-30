import asyncio

from hexi.plugin.InputPlugin import InputPlugin
from hexi.service import event
from plugins.input_fsx.FsxDataUdpServer import FsxDataUdpServer

class PluginInputFsx(InputPlugin):
  def __init__(self):
    super().__init__();
    self.configurable = True
    self.clientIp = None
    self.clientId = None
    self.createUdpServer()

  def createUdpServer(self):
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(FsxDataUdpServer, local_addr=('0.0.0.0', 4980))
    asyncio.ensure_future(listen)
