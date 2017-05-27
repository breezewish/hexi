from hexi.service import event
from hexi.service import plugin
from hexi.plugin.McaPlugin import McaPlugin


def init():
  event.subscribe(onPipelineSrcData, ['hexi.pipeline.src.data'])
  plugin.addCategory('mca', McaPlugin)

async def onPipelineSrcData(e):
  pass
