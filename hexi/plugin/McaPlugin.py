from hexi.plugin.BasePlugin import BasePlugin
from hexi.service import event


class MCAPlugin(BasePlugin):
  def activate(self):
    super().activate()
    event.subscribe(self.on_input_signal, ['hexi.pipeline.input.data'])

  def deactivate(self):
    super().deactivate()
    event.unsubscribe(self.on_input_signal)

  def handle_input_signal(self, signal):
    raise

  async def on_input_signal(self, e):
    self.handle_input_signal(e['value'])
