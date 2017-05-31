from sanic.response import json
from hexi.service import event
from hexi.service.pipeline.BaseManager import BaseManager
from hexi.plugin.MCAPlugin import MCAPlugin


class MCAManager(BaseManager):
  def __init__(self):
    super().__init__('mca', 'mca', MCAPlugin)

  def init(self):
    super().init()

