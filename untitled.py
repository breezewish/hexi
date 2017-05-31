from scipy import signal

import numpy as np
import matplotlib.pyplot as plt
import profile


class RealtimeFilter():
  def __init__(self, b, a):
    assert(len(b) == len(a))
    self.n = len(b) # n = order + 1
    self.b = b
    self.a = a
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

# 2nd-order LP

w_lp = 5.0
t_lp = 1.0

b_lp = [0, 0, w_lp ** 2]
a_lp = [1, 2 * t_lp * w_lp, w_lp ** 2]

# 2nd-order HP

w_hp = 2.5
t_hp = 1.0

b_hp = [1, 0, 0]
a_hp = [1, 2 * t_hp * w_hp, w_lp ** 2]

# 3nd-order HP

w_n_hp_3 = 2.5
w_b_hp_3 = 2.5
t_hp_3 = 1.0

b_hp_3 = [1, 0, 0, 0]
a_hp_3 = [1, 2 * t_hp_3 * w_n_hp_3 + w_b_hp_3, w_n_hp_3 ** 2 + w_b_hp_3 * 2 * t_hp_3 * w_n_hp_3, w_n_hp_3 ** 2 * w_b_hp_3]

b2_lp, a2_lp = signal.bilinear(b_lp, a_lp, fs=100)


b2_hp, a2_hp = signal.bilinear(b_hp, a_hp, fs=100)
b2_hp_3, a2_hp_3 = signal.bilinear(b_hp_3, a_hp_3, fs=100)
filter_hp_3 = RealtimeFilter(b2_hp_3, a2_hp_3)
#print(b2_lp)
#print(a2_lp)

impulse = np.zeros(20 * 100, dtype=np.float)
x = np.zeros(20 * 100, dtype=np.float)
for i in range(0, 20 * 100):
  x[i] = i / 100
for i in range(100, 200):
  impulse[i] = (i - 100) / 100 * 6
for i in range(200, 700):
  impulse[i] = 6
for i in range(700, 800):
  impulse[i] = 6 - ((i - 700) / 100 * 6)


impulse_sample = np.zeros(20 * 10, dtype=np.float)
x_sample = np.zeros(20 * 10, dtype=np.float)
for i in range(0, 20 * 10):
  x_sample[i] = i / 10
for i in range(0, 20 * 10):
  impulse_sample[i] = impulse[i * 10]

#for i in range(0, 20 * 100):
#  print(x[i], impulse[i])


def run():
  h_lp = signal.lfilter(b2_lp, a2_lp, impulse)
  h_hp = signal.lfilter(b2_hp, a2_hp, impulse)
  h_hp_3 = signal.lfilter(b2_hp_3, a2_hp_3, impulse)
  h_hp_3_realtime = np.zeros(20 * 100, dtype=np.float)
  for i in range(0, 20 * 100):
    h_hp_3_realtime[i] = filter_hp_3.apply(impulse[i]) + 1
  #h_lp_sample = signal.lfilter(b2_lp, a2_lp, impulse_sample)
  return h_lp, h_hp, h_hp_3, h_hp_3_realtime

def integrate(arr):
  output_arr = np.zeros(len(arr), dtype=np.float)
  sum_val = 0
  for idx, val in enumerate(arr):
    sum_val += val
    output_arr[idx] = sum_val
  return output_arr

profile.run('run()')

h_lp, h_hp, h_hp_3, h_hp_3_realtime = run()
fig, ax = plt.subplots()

disp_hp = integrate(integrate(h_hp))
disp_hp_3 = integrate(integrate(h_hp_3))

ax.plot(x, impulse, ':', label='Input Signal')
ax.plot(x_sample, impulse_sample, ':', label='Input Signal (Sampled)')
#ax.plot(x, h_lp, ':', label='2rd-order LP')
#ax.plot(x, h_hp, ':', label='2rd-order HP')
ax.plot(x, h_hp_3, ':', label='3rd-order HP')
ax.plot(x, h_hp_3_realtime, ':', label='3rd-order HP (RealTime)')
#ax.plot(x_sample, h_lp_sample, ':', label='3rd-order HP')
#ax.plot(x, disp_hp, label='2rd-order HP Displacement')
#ax.plot(x, disp_hp_3, label='3rd-order HP Displacement')
ax.legend(loc='lower right')

plt.show()




"""
plt.plot(x, impulse)
plt.xlabel('time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid(True)
plt.show()
"""

"""
plt.plot(x, h)
plt.xlabel('time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid(True)
plt.show()
"""
