from hexi.service import event
from hexi.service import plugin
from hexi.plugin.McaPlugin import McaPlugin


def init():
  event.subscribe(onPipelineInputData, ['hexi.pipeline.input.data'])
  plugin.addCategory('mca', McaPlugin)

async def onPipelineInputData(e):
  pass
