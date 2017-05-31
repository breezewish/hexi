import asyncio
import ipaddress
import collections
import logging
import numpy
import scipy.constants

from sanic.response import json
from hexi.plugin.MCAPlugin import MCAPlugin
from hexi.service import event

_logger = logging.getLogger(__name__)

VECTOR_G = np.array([0, 0, scipy.constants.g])
ps = np.array([0, 0, 0]) # 平台位置
po = np.array([0, 0, 0]) # 平台旋转角度


class PluginMCAClassicalWashout(MCAPlugin):

  def __init__(self):
    super().__init__()
    self.configurable = True
    self.config_default = {
      'scale': {
        'type': 'third-order',  # ['third-order', 'linear']
        'src_max': {
          'x': 10,
          'y': 10,
          'z': 10,
          'alpha': 10,
          'beta': 10,
          'gamma': 10,
        },  # 在运行时根据数据调整最大值
      }
    }
    self.

  def load(self):
    super().load()

    @self.bp.route('/api/config/scale', methods=['GET'])
    async def get_scale_config(request):
      return json({ 'code': 200, 'data': self.config['scale'] })

    @self.bp.route('/api/config/scale', methods=['POST'])
    async def set_scale_config(request):
      try:
        self.config['scale']['type'] = request.json['type']
        return json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return json({ 'code': 400, 'reason': str(e) })

  def _update_scale(self, data):
    scales = self.config['scale']['src_max']
    for key in ['x', 'y', 'z', 'alpha', 'beta', 'gamma']:
      value = abs(data[key])
      if value > scales[key]:
        scales[key] = value

  def handle_input_signal(self, signal_data):
    self._update_scale(signal_data)

    # 绝对线加速度
    a_a = np.array([signal_data.x, signal_data.y, signal_data.z])

    # 角速度
    omega_a = np.array([signal_data.alpha, signal_data.beta, signal_data.gamma])

    # 比力
    f_a = a_a

    signal = self.scale_signal(signal)
    print(x, y, z, alpha, beta, gamma)
    pass
