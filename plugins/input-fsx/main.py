from hexi.plugin.InputPlugin import InputPlugin
from hexi.service import event


class PluginInputFsx(InputPlugin):
  def __init__(self):
    self.configurable = True

  def print_name(self):
    print(event)
    print("FSX")

  def activate(self):
    print('activate FSX')
    super().activate()

  def deactivate(self):
    print('deactivate FSX')
    super().deactivate()
