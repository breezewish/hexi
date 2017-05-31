from hexi.service.pipeline.BaseManager import BaseManager
from hexi.plugin.OutputPlugin import OutputPlugin


class OutputManager(BaseManager):
  def __init__(self):
    super().__init__('output', 'output', OutputPlugin)
