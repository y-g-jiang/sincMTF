import numpy as np
import matplotlib.pyplot as plt
import os, PyQt5
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    os.path.dirname(PyQt5.__file__), 'Qt5', 'plugins', 'platforms')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  
matplotlib.rcParams['axes.unicode_minus'] = False    

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

x1 = np.array([0.13, 19.95, 40.03, 60.10, 80.05, 100.25, 71.46, 52.15, 100.13,
               90.78, 109.97, 120.08, 129.42, 140.03, 149.87, 157.58, 161.62, 165.40, 167.93])
y1 = np.array([1.000, 0.930, 0.806, 0.648, 0.484, 0.341, 0.554, 0.713, 0.342,
               0.411, 0.277, 0.217, 0.167, 0.119, 0.080, 0.055, 0.037, 0.028, 0.021])

x2 = np.array([0.13, 20.05, 39.97, 29.63, 44.77, 54.35, 59.90, 79.95, 71.25, 87.64,
               99.87, 108.20, 116.90, 128.63, 139.85, 148.30, 159.65, 166.33])
y2 = np.array([0.997, 0.921, 0.778, 0.858, 0.741, 0.653, 0.602, 0.420, 0.500, 0.358,
               0.273, 0.226, 0.176, 0.120, 0.076, 0.048, 0.025, 0.014])

sort_idx1 = np.argsort(x1)
x1, y1 = x1[sort_idx1], y1[sort_idx1]

sort_idx2 = np.argsort(x2)
x2, y2 = x2[sort_idx2], y2[sort_idx2]

# 插值到统一频率网格

x_common = np.linspace(0, max(max(x1), max(x2)), 300)
y1_interp = np.interp(x_common, x1, y1)
y2_interp = np.interp(x_common, x2, y2)

def sinc_func(f, a, b):
    return np.sinc(b * f) * a
fig, ax = plt.subplots(figsize=(8,5))
plt.subplots_adjust(bottom=0.25)

line1, = ax.plot(x_common, y1_interp, 'b-', label='SFR1')
line2, = ax.plot(x_common, y2_interp, 'g-', label='SFR2')
sinc_line, = ax.plot(x_common, y1_interp * sinc_func(x_common, 0.5, 0.05), 'r--', label='SFR1*sinc')

ax.set_xlabel('Frequency')
ax.set_ylabel('MTF')
ax.set_title('SFR1, SFR2 与 SFR1*sinc 交互调整')
ax.grid(True)
ax.legend()
axcolor = 'lightgoldenrodyellow'
ax_amp = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)

slider_amp = Slider(ax_amp, '幅度 a', 0.0, 1.0, valinit=0.5)
slider_freq = Slider(ax_freq, '频率 b', 0.001, 0.2, valinit=0.05)

# Slider 更新回调

def update(val):
    a = slider_amp.val
    b = slider_freq.val
    sinc_line.set_ydata(y1_interp * sinc_func(x_common, a, b))
    fig.canvas.draw_idle()

slider_amp.on_changed(update)
slider_freq.on_changed(update)

plt.show()
