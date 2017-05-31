import asyncio
import ipaddress
import collections
import logging
import math
import numpy
import scipy.constants
import time

from sanic.response import json
from hexi.plugin.MCAPlugin import MCAPlugin
from hexi.service import event
from plugins.mca_classical_washout import dfilter

_logger = logging.getLogger(__name__)

VECTOR_G = numpy.array([[0, 0, scipy.constants.g]]).T

coll_2lp = []
coll_3hp = []
coll_s = []
coll_theta_tc = []


class PluginMCAClassicalWashout(MCAPlugin):

  def __init__(self):
    super().__init__()
    self.configurable = True
    self.config_default = {
      'freq': 20,
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
      },
      'filter': {
        'tilt': {
          'x': {
            'order': 2,
            'lp': True,
            'zeta': 1.0,
            'omega': 5.0,
          },
          'y': {
            'order': 2,
            'lp': True,
            'zeta': 1.0,
            'omega': 8.0,
          },
        },
        'movement': {
          'x': {
            'order': 3,
            'lp': False,
            'zeta': 1.0,
            'omega': 2.5,
            'omega_1': 0.25,
          },
          'y': {
            'order': 3,
            'lp': False,
            'zeta': 1.0,
            'omega': 4.0,
            'omega_1': 0.4,
          },
          'z': {
            'order': 3,
            'lp': False,
            'zeta': 1.0,
            'omega': 4.0,
            'omega_1': 0.4,
          },
        },
        'rotate': {
          'alpha': {
            'order': 1,
            'lp': False,
            'omega': 1.0,
          },
          'beta': {
            'order': 1,
            'lp': False,
            'omega': 1.0,
          },
          'gamma': {
            'order': 2,
            'lp': False,
            'zeta': 1.0,
            'omega': 1.0,
          },
        },
      },
    }

  def rebuild_filters(self):
    self.filters = {}
    for kind, dimensions in self.config['filter'].items():
      self.filters[kind] = {}
      for d, filter_config in dimensions.items():
        self.filters[kind][d] = dfilter.build_filter(**filter_config)

  def load(self):
    super().load()

    self.rebuild_filters()
    self.reset()

    @self.bp.route('/api/config/scale', methods=['GET'])
    async def get_scale_config(request):
      return json({ 'code': 200, 'data': self.config['scale'] })

    @self.bp.route('/api/config/scale', methods=['POST'])
    async def set_scale_config(request):
      try:
        self.config['scale']['type'] = request.json['type']
        # TODO: save config
        return json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return json({ 'code': 400, 'reason': str(e) })

    @self.bp.route('/api/config/filter', methods=['GET'])
    async def get_scale_config(request):
      return json({ 'code': 200, 'data': self.config['filter'] })

    @self.bp.route('/api/config/filter', methods=['POST'])
    async def set_scale_config(request):
      try:
        self.config['filter'] = request.json
        self.rebuild_filters()
        # TODO: save config
        return json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return json({ 'code': 400, 'reason': str(e) })

    # TODO: remove this!!!!
    ########
    FREQ = 20
    impulse = numpy.zeros(20 * FREQ, dtype=numpy.float)
    x = numpy.zeros(20 * FREQ, dtype=numpy.float)
    for i in range(0, 20 * FREQ):
      x[i] = i / FREQ
    for i in range(1 * FREQ, 2 * FREQ):
      impulse[i] = (i - 1 * FREQ) / FREQ * 6
    for i in range(2 * FREQ, 7 * FREQ):
      impulse[i] = 6
    for i in range(7 * FREQ, 8 * FREQ):
      impulse[i] = 6 - ((i - 7 * FREQ) / FREQ * 6)


    print(time.time())

    for i in range(0, 20 * FREQ):
      self.handle_input_signal([impulse[i], 0, 0, 0, 0, 0])

    print(time.time())

    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(x, impulse, label='Input Signal')
    ax.plot(x, coll_s, label='S')
    ax.plot(x, coll_theta_tc, label='theta')
    ax.legend(loc='lower right')
    plt.show()
    """

    ########

  def _update_scale(self, data):
    scales = self.config['scale']['src_max']
    for index, key in enumerate(['x', 'y', 'z', 'alpha', 'beta', 'gamma']):
      value = abs(data[index])
      if value > scales[key]:
        scales[key] = value

  def apply_movement_filter(self, a_i):
    filters = self.filters['movement']
    return numpy.array([[
        filters['x'].apply(a_i[0][0]),
        filters['y'].apply(a_i[1][0]),
        filters['z'].apply(a_i[2][0]),
      ]]).T

  def apply_tilt_filter(self, f_s):
    filters = self.filters['tilt']
    return numpy.array([[
        filters['x'].apply(f_s[0][0]),
        filters['y'].apply(f_s[1][0]),
        0,
      ]]).T

  def apply_rotate_filter(self, omega_s):
    filters = self.filters['rotate']
    return numpy.array([[
        filters['alpha'].apply(omega_s[0][0]),
        filters['beta'].apply(omega_s[1][0]),
        filters['gamma'].apply(omega_s[2][0]),
      ]]).T

  def reset(self):
    global ig_disp_1, ig_disp_2, ig_rot_1, ps, po
    ig_disp_1 = numpy.array([[0, 0, 0]]).T  # 位移运动一次积分
    ig_disp_2 = numpy.array([[0, 0, 0]]).T  # 位移运动二次积分
    ig_rot_1 = numpy.array([[0, 0, 0]]).T   # 旋转运动一次积分
    ps = numpy.array([[0, 0, 0]]).T         # 平台位置（ps = ig_disp_2）
    po = numpy.array([[0, 0, 0]]).T         # 平台旋转角度

    # 重置滤波器内部状态
    for kind, dimensions in self.config['filter'].items():
      for d, filter_config in dimensions.items():
        self.filters[kind][d].reset()


  def handle_input_signal(self, data):
    global ig_disp_1, ig_disp_2, ig_rot_1, ps, po

    delta_time = 1 / self.config['freq']

    # 更新缩放最大值
    self._update_scale(data)

    # 旋转矩阵
    r_x = numpy.array([
      [1, 0, 0],
      [0, math.cos(po[0][0]), math.sin(po[0][0])],
      [0, -math.sin(po[0][0]), math.cos(po[0][0])],
    ])
    r_y = numpy.array([
      [math.cos(po[1][0]), 0, -math.sin(po[1][0])],
      [0, 1, 0],
      [math.sin(po[1][0]), 0, math.cos(po[1][0])],
    ])
    r_z = numpy.array([
      [math.cos(po[2][0]), math.sin(po[2][0]), 0],
      [-math.sin(po[2][0]), math.cos(po[2][0]), 0],
      [0, 0, 1],
    ])
    L = r_x * r_y * r_z

    # 体坐标系下重力加速度
    g_a = L * VECTOR_G

    # 绝对线加速度
    a_a = numpy.array([data[0:3]]).T

    # 角速度
    omega_a = numpy.array([data[3:6]]).T

    # 比力
    f_a = a_a - g_a

    #####################

    # 位移运动：缩放
    # TODO
    f_s = f_a

    # 位移运动：变幻
    f_i = L * f_s
    a_i = f_i + VECTOR_G

    # 位移运动：高通滤波
    a_hp = self.apply_movement_filter(a_i)

    # 位移运动：积分
    ig_disp_1 = ig_disp_1 + delta_time * a_hp       # 第一次积分
    ig_disp_2 = ig_disp_2 + delta_time * ig_disp_1  # 第二次积分
    ps = ig_disp_2

    #####################

    # 倾斜协调：低通滤波
    f_lp = self.apply_tilt_filter(f_s)

    # 倾斜协调：计算（公式2.29）
    theta_lp = numpy.array([[
      math.asin(f_lp[1][0] / scipy.constants.g),
      -math.asin(f_lp[0][0] / scipy.constants.g),
      0
    ]]).T

    # 倾斜协调：限速
    # TODO
    theta_tc = theta_lp

    #####################

    # 旋转运动：缩放
    # TODO
    omega_s = omega_a

    # 旋转运动：高通滤波
    omega_hp = self.apply_rotate_filter(omega_s)

    # 旋转运动：积分
    ig_rot_1 = ig_rot_1 + delta_time * omega_hp    # 一次积分

    #####################

    po = ig_rot_1 + theta_tc

    self.emit_mca_signal(data, [
      ps[0][0],
      ps[1][0],
      ps[2][0],
      po[0][0],
      po[1][0],
      po[2][0],
    ])

    #coll_2lp.append(f_lp[0][0])
    #coll_3hp.append(a_hp[0][0])
    #coll_s.append(ps[0][0])
    #coll_theta_tc.append(theta_lp[1][0])
