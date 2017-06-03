import asyncio
import ipaddress
import collections
import logging
import math
import numpy
import scipy.constants
import time

from sanic import response
from hexi.plugin.MCAPlugin import MCAPlugin
from hexi.service import event
from plugins.mca_classical_washout import dfilter

_logger = logging.getLogger(__name__)

VECTOR_G = numpy.array([[0, 0, scipy.constants.g]]).T
MAX_MOVE_ACCELERATION = 1                 # in meters
MAX_ROTATE_VELOCITY = numpy.deg2rad(10)   # in degree
MAX_TILT_ACCELERATION = math.sin(numpy.deg2rad(30)) * scipy.constants.g

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
          'x': 0,
          'y': 0,
          'z': 0,
          'alpha': 0,
          'beta': 0,
          'gamma': 0,
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
      return response.json({ 'code': 200, 'data': self.config['scale'] })

    @self.bp.route('/api/config/scale', methods=['POST'])
    async def set_scale_config(request):
      try:
        self.config['scale']['type'] = request.json['type']
        # TODO: save config
        return response.json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return response.json({ 'code': 400, 'reason': str(e) })

    @self.bp.route('/api/config/filter', methods=['GET'])
    async def get_scale_config(request):
      return response.json({ 'code': 200, 'data': self.config['filter'] })

    @self.bp.route('/api/config/filter', methods=['POST'])
    async def set_scale_config(request):
      try:
        self.config['filter'] = request.json
        self.rebuild_filters()
        # TODO: save config
        return response.json({ 'code': 200 })
      except Exception as e:
        _logger.exception('Save config failed')
        return response.json({ 'code': 400, 'reason': str(e) })

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

  def apply_scaling(self, x, max_x, max_y):
    if max_x == 0:
      return 0
    sign = numpy.sign(x)
    if abs(x) > max_x:
      return sign * max_y
    else:
      return (max_y / max_x) * x

  def apply_movement_scaling(self, vector):
    # TODO: fix me. currently using a fixed max_x
    ret = numpy.copy(vector)
    scale_opt = self.config['scale']['src_max']
    ret[0][0] = self.apply_scaling(vector[0][0], 3, MAX_MOVE_ACCELERATION)
    ret[1][0] = self.apply_scaling(vector[1][0], 3, MAX_MOVE_ACCELERATION)
    #ret[2][0] = self.apply_scaling(vector[2][0], scale_opt['z'], MAX_MOVE_ACCELERATION)
    return ret

  def apply_rotate_scaling(self, vector):
    # TODO: fix me. currently using a fixed max_x
    ret = numpy.copy(vector)
    scale_opt = self.config['scale']['src_max']
    ret[0][0] = self.apply_scaling(vector[0][0], 2, MAX_ROTATE_VELOCITY)
    ret[1][0] = self.apply_scaling(vector[1][0], 2, MAX_ROTATE_VELOCITY)
    ret[2][0] = self.apply_scaling(vector[2][0], 2, MAX_ROTATE_VELOCITY)
    return ret

  def apply_tilt_scaling(self, scalar):
    return scalar * (MAX_TILT_ACCELERATION / MAX_MOVE_ACCELERATION)
    """
    sign = numpy.sign(scalar)
    if abs(scalar) > MAX_TILT_ACCELERATION:
      return sign * MAX_TILT_ACCELERATION
    else:
      return scalar
    """

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
    L = r_x.dot(r_y).dot(r_z)

    # 体坐标系下重力加速度
    g_a = L.dot(VECTOR_G)

    # 绝对线加速度
    a_a = numpy.array([data[0:3]]).T

    # 角速度
    omega_a = numpy.array([data[3:6]]).T

    # 比力
    f_a = a_a - g_a

    #####################

    # 位移运动：缩放
    f_s = self.apply_movement_scaling(f_a)

    # 位移运动：变幻
    f_i = L.dot(f_s)
    a_i = f_i + VECTOR_G

    # 位移运动：高通滤波
    a_hp = self.apply_movement_filter(a_i)

    # 位移运动：积分
    ig_disp_1 = ig_disp_1 + delta_time * a_hp       # 第一次积分
    ig_disp_2 = ig_disp_2 + delta_time * ig_disp_1  # 第二次积分
    ps = numpy.copy(ig_disp_2)

    #####################

    # 倾斜协调：低通滤波
    f_lp = self.apply_tilt_filter(f_s)

    # 倾斜协调：计算（公式2.29）
    theta_lp = numpy.array([[
      math.asin(self.apply_tilt_scaling(f_lp[1][0]) / scipy.constants.g),
      -math.asin(self.apply_tilt_scaling(f_lp[0][0]) / scipy.constants.g),
      0
    ]]).T

    # 倾斜协调：限速
    # TODO
    theta_tc = theta_lp

    #####################

    # 旋转运动：缩放
    omega_s = self.apply_rotate_scaling(omega_a)

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
