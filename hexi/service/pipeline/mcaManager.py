from hexi.service import event
from hexi.service import plugin
from hexi.plugin.McaPlugin import McaPlugin


def init():
  event.subscribe(on_pipeline_input_data, ['hexi.pipeline.input.data'])
  plugin.addCategory('mca', McaPlugin)

async def on_pipeline_input_data(e):
  pass
