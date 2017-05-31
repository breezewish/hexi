from scipy import signal

import numpy as np
import matplotlib.pyplot as plt
import profile

FREQ = 20

# 2nd-order LP

w_lp = 5.0
t_lp = 1.0

b_lp = [0, 0, w_lp ** 2]
a_lp = [1, 2 * t_lp * w_lp, w_lp ** 2]

# 3nd-order HP

w_n_hp_3 = 2.5
w_b_hp_3 = 0.25
t_hp_3 = 1.0

b_hp_3 = [1, 0, 0, 0]
a_hp_3 = [1, 2 * t_hp_3 * w_n_hp_3 + w_b_hp_3, w_n_hp_3 ** 2 + w_b_hp_3 * 2 * t_hp_3 * w_n_hp_3, w_n_hp_3 ** 2 * w_b_hp_3]

b2_lp, a2_lp = signal.bilinear(b_lp, a_lp, fs=FREQ)
b2_hp_3, a2_hp_3 = signal.bilinear(b_hp_3, a_hp_3, fs=FREQ)


impulse = np.zeros(20 * FREQ, dtype=np.float)
x = np.zeros(20 * FREQ, dtype=np.float)
for i in range(0, 20 * FREQ):
  x[i] = i / FREQ
for i in range(1 * FREQ, 2 * FREQ):
  impulse[i] = (i - 1 * FREQ) / FREQ * 6
for i in range(2 * FREQ, 7 * FREQ):
  impulse[i] = 6
for i in range(7 * FREQ, 8 * FREQ):
  impulse[i] = 6 - ((i - 7 * FREQ) / FREQ * 6)

h_lp = signal.lfilter(b2_lp, a2_lp, impulse)
h_hp_3 = signal.lfilter(b2_hp_3, a2_hp_3, impulse)

fig, ax = plt.subplots()

ax.plot(x, impulse, label='Input Signal')
ax.plot(x, h_lp, label='2rd-order LP')
#ax.plot(x, h_hp, label='2rd-order HP')
ax.plot(x, h_hp_3, label='3rd-order HP')
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
