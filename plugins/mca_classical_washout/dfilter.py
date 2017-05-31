import numpy as np

from scipy import signal

FREQ = 20


class RealtimeFilter():
  def __init__(self, b, a):
    assert(len(b) == len(a))
    self.n = len(b) # n = order + 1
    self.b = b
    self.a = a
    self.reset()

  def reset(self):
    self.input = np.zeros(self.n, dtype=np.float)
    self.output = np.zeros(self.n, dtype=np.float)

  def apply(self, v):
    self.input[self.n - 1] = v
    self.output[self.n - 1] = 0
    output = 0
    for i in range(0, self.n):
      output = output + \
        self.b[i] * self.input[self.n - 1 - i] - \
        self.a[i] * self.output[self.n - 1 - i]
    self.output[self.n - 1] = output
    for i in range(0, self.n - 1):
      self.input[i] = self.input[i+1]
      self.output[i] = self.output[i+1]
    return output


def build_1st_filter(omega, lp=True, freq=FREQ):
  b = [1, 0] if not lp else [0, omega]
  a = [1, omega]
  return RealtimeFilter(*signal.bilinear(b, a, fs=freq))


def build_2nd_filter(omega, zeta, lp=True, freq=FREQ):
  b = [1, 0, 0] if not lp else [0, 0, omega ** 2]
  a = [1, 2 * zeta * omega, omega ** 2]
  return RealtimeFilter(*signal.bilinear(b, a, fs=freq))


def build_3rd_filter(omega, zeta, omega_1, lp=True, freq=FREQ):
  b = [1, 0, 0, 0] if not lp else [0, 0, 0, omega ** 3]
  a = [1, 2 * zeta * omega + omega_1, omega ** 2 + omega_1 * 2 * zeta * omega, omega ** 2 * omega_1]
  return RealtimeFilter(*signal.bilinear(b, a, fs=freq))


def build_filter(*, order:int=1, lp:bool=True,
  omega:float=0.0, zeta:float=1.0, omega_1:float=0.0, freq=FREQ):
  assert order in [1, 2, 3]
  if order == 1:
    return build_1st_filter(omega, lp, freq)
  elif order == 2:
    return build_2nd_filter(omega, zeta, lp, freq)
  else:
    return build_3rd_filter(omega, zeta, omega_1, lp, freq)

