from scipy import signal

import numpy as np
import matplotlib.pyplot as plt

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

for i in range(0, 20 * 100):
  print(x[i], impulse[i])

h_lp = signal.lfilter(b2_lp, a2_lp, impulse)
h_hp = signal.lfilter(b2_hp, a2_hp, impulse)
h_hp_3 = signal.lfilter(b2_hp_3, a2_hp_3, impulse)

fig, ax = plt.subplots()
#ax.plot(x, impulse, label='Input Signal')
#ax.plot(x, h_lp, label='2rd-order LP')
#ax.plot(x, h_hp, label='2rd-order HP')
#ax.plot(x, h_hp_3, label='3rd-order HP')


def integrate(arr):
  output_arr = np.zeros(len(arr), dtype=np.float)
  sum_val = 0
  for idx, val in enumerate(arr):
    sum_val += val
    output_arr[idx] = sum_val
  return output_arr

disp_hp = integrate(integrate(h_hp))
disp_hp_3 = integrate(integrate(h_hp_3))

ax.plot(x, disp_hp, label='2rd-order HP Displacement')
ax.plot(x, disp_hp_3, label='3rd-order HP Displacement')
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
