import tkinter as tk
import random
import tempfile
import os
from PIL import Image, ImageSequence
import win32gui

# Get window size
# 获取当前活动窗口的句柄
hwnd = win32gui.GetForegroundWindow()

# 获取窗口矩形（左、上、右、下）
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

# 计算宽度和高度
width = right - left
height = bottom - top

# Initial state
x = int(width * 0.85)
y = int(height * 0.75)
cycle = 0
check = 0
event_number = random.choice([0, 1, 2, 3])

# Path to GIFs (make sure they are in this folder)
impath = "assets/"

# Create Tkinter window
window = tk.Tk()
window.overrideredirect(True)               # 移除窗口边框
window.wm_attributes("-topmost", True)      # 窗口始终置顶
window.wm_attributes("-transparentcolor", "black")  # 启用透明背景
window.configure(bg='black')                # 设置背景颜色

# Load slime GIF frames
def load_full_gif_frames(path):
    frames = []
    with Image.open(path) as im:
        for i, frame in enumerate(ImageSequence.Iterator(im)):
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                # 保存为 PNG（保留透明通道）
                frame.save(tmp, format="PNG")
                tmp_path = tmp.name
            
            # 加载 PNG 文件
            photo = tk.PhotoImage(file=tmp_path)
            
            # 添加到帧列表
            frames.append(photo)
            
            # 删除临时文件（Tkinter 会缓存图像）
            os.remove(tmp_path)
    
    return frames

# 加载动画帧
impath = "assets/"
slime_original = load_full_gif_frames(impath + "Slime_Original.gif")
slime_jiggling = load_full_gif_frames(impath + "Slime_Jiggling.gif")
slime_looking = load_full_gif_frames(impath + "Slime_Looking_Around.gif")
slime_blinking = load_full_gif_frames(impath + "Slime_Blinking.gif")

# Combine all actions for easier switching
animations = {
    0: slime_original,
    1: slime_jiggling,
    2: slime_looking,
    3: slime_blinking
}

# Display slime image
label = tk.Label(window, bd=0, bg="black")
label.pack()

# Function to animate slime
def update(cycle, event_number, x):
    frames = animations[event_number]
    
    # Update frame
    frame = frames[cycle]
    label.configure(image=frame)
    window.geometry(f"256x256+{x}+{y}")

    # Move to next frame
    cycle += 1
    if cycle >= len(frames):
        cycle = 0
        event_number = random.choice(list(animations.keys()))  # pick a new action

    window.after(150, update, cycle, event_number, x)

# Start the loop
window.after(0, update, cycle, event_number, x)
window.mainloop()
