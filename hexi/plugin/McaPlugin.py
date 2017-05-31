import asyncio

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

  def emit_mca_signal(self, input_data, mca_data):
    """
      input_data should be [x, y, z, alpha, beta, gamma]
      mca_data should be [s_x, s_y, s_z, theta_alpha, theta_beta, theta_gamma]
    """
    asyncio.ensure_future(event.publish('hexi.pipeline.mca.raw_data', (input_data, mca_data)))

