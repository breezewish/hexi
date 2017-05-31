from sanic.response import json
from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.plugin.OutputPlugin import OutputPlugin


class OutputManager(BaseManager):
  def __init__(self):
    super().__init__('output', 'output', OutputPlugin)

  def init(self):
    super().init()

