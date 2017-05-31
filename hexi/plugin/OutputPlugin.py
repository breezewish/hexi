from hexi.plugin.BasePlugin import BasePlugin
from hexi.service import event


class OutputPlugin(BasePlugin):
  def activate(self):
    super().activate()
    event.subscribe(self._on_mca_signal, ['hexi.pipeline.mca.data'])

  def deactivate(self):
    super().deactivate()
    event.unsubscribe(self._on_mca_signal)

  async def _on_mca_signal(self, e):
    input_signal, motion_signal = e['value']
    self.handle_motion_signal(input_signal, motion_signal)

  def handle_motion_signal(self, input_signal, motion_signal):
    raise
