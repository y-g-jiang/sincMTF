import numpy as np
import matplotlib.pyplot as plt
import os, PyQt5
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    os.path.dirname(PyQt5.__file__), 'Qt5', 'plugins', 'platforms')
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import matplotlib

# ===========================
# 强制使用 SimHei 中文字体，避免警告
# ===========================
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ===========================
# 1️⃣ 打开文件选择对话框
# ===========================
root = Tk()
root.withdraw()  # 隐藏主窗口
img_path = filedialog.askopenfilename(
    title="选择 MTF 曲线图文件",
    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
)
if not img_path:
    print("未选择文件，程序退出")
    exit()

# ===========================
# 2️⃣ 初始化变量
# ===========================
points = []
click_count = 0
coords_dict = {}

# ===========================
# 3️⃣ 鼠标点击事件回调
# ===========================
def onclick(event):
    global click_count, coords_dict, points
    if event.xdata is None or event.ydata is None:
        return

    click_count += 1

    if click_count == 1:
        coords_dict['y0'] = (event.x, event.y)
        print("点击纵轴下端 MTF=0 的位置")
    elif click_count == 2:
        coords_dict['y1'] = (event.x, event.y)
        print("点击纵轴上端 MTF=1 的位置")
    elif click_count == 3:
        coords_dict['x0'] = (event.x, event.y)
        print("点击横轴左端 0 的位置")
    elif click_count == 4:
        coords_dict['x100'] = (event.x, event.y)
        print("点击横轴右端 100 的位置")
    else:
        points.append((event.x, event.y))
        print(f"第 {click_count-4} 个曲线点：像素坐标 ({event.x:.1f}, {event.y:.1f})")

# ===========================
# 4️⃣ 显示图像并绑定点击
# ===========================
img = plt.imread(img_path)
fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("依次点击：纵轴下0 → 纵轴上1 → 横轴左0 → 横轴右100 → 曲线点，关闭窗口完成")
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
fig.canvas.mpl_disconnect(cid)

# ===========================
# 5️⃣ 像素坐标转换为实际数值
# ===========================
y0_px, y0_py = coords_dict['y0']
y1_px, y1_py = coords_dict['y1']
x0_px, x0_py = coords_dict['x0']
x100_px, x100_py = coords_dict['x100']

# 横纵轴映射比例
x_scale = 100 / (x100_px - x0_px)           # 横轴 0→100
y_scale = 1.0 / (y1_py - y0_py)             # 纵轴 0→1

digitized_points = []
print("\n数字化曲线坐标 (x, y):")
for i, (px, py) in enumerate(points, start=1):
    x_val = (px - x0_px) * x_scale
    y_val = (py - y0_py) * y_scale
    digitized_points.append((x_val, y_val))
    print(f"点 {i}: x = {x_val:.2f}, y = {y_val:.3f}")
