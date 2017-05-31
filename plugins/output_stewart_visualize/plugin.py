import asyncio
import logging

from sanic.response import json
from hexi.plugin.OutputPlugin import OutputPlugin

_logger = logging.getLogger(__name__)


class PluginOutputStewartVisualize(OutputPlugin):

  def __init__(self):
    super().__init__()
    self.configurable = True

  def handle_motion_signal(self, input_signal, motion_signal):
    pass
