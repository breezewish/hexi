from hexi.service import event
from hexi.service import plugin
from hexi.plugin.OutputPlugin import OutputPlugin


def init():
  event.subscribe(onPipelineMcaData, ['hexi.pipeline.mca.data'])
  plugin.addCategory('output', OutputPlugin)

async def onPipelineMcaData(e):
  pass
