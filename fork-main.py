import tkinter as tk
import random
import time
from PIL import Image, ImageSequence, ImageOps
import win32gui
import tempfile
import os
import ss
import xy

# 获取窗口尺寸
hwnd = win32gui.GetForegroundWindow()
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
width = right - left
height = bottom - top

# 初始位置
x = int(width * 0.1)
y = int(height * 0.75)

# 初始化参数
cd_duration = 500000 # 特殊行动共享CD（毫秒）
last_special_time = 0  # 上次执行特殊行动的时间

# Tkinter窗口配置
window = tk.Tk()
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "black")
window.configure(bg='black')

# 加载GIF帧函数
def load_full_gif_frames(path, flip=False):
    frames = []
    with Image.open(path) as im:
        for frame in ImageSequence.Iterator(im):
            if flip:
                frame = ImageOps.mirror(frame)  # 翻转当前帧

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                frame.save(tmp, format="PNG")
                tmp_path = tmp.name

            photo = tk.PhotoImage(file=tmp_path)
            frames.append(photo)
            os.remove(tmp_path)

    return frames

# 动画资源路径
impath = "assets/"
animations = {
    0 : load_full_gif_frames(impath + "Slime_Balloon_Flying.gif"),
    1 : load_full_gif_frames(impath + "Slime_Balloon_Off.gif"),
    2 : load_full_gif_frames(impath + "Slime_Balloon_On.gif"),
    3 : load_full_gif_frames(impath + "Slime_Blinking.gif"),
    4 : load_full_gif_frames(impath + "Slime_Change_Heart.gif"),
    5 : load_full_gif_frames(impath + "Slime_Close_Eye.gif"),
    6 : load_full_gif_frames(impath + "Slime_Eating_Angry.gif"),
    7 : load_full_gif_frames(impath + "Slime_Eating_Friendly_Portal.gif"),
    7 : load_full_gif_frames(impath + "Slime_Eating_Friendly.gif"),
    8 : load_full_gif_frames(impath + "Slime_Go_Boom.gif"),
    9 : load_full_gif_frames(impath + "Slime_Hungry.gif"),
    10: load_full_gif_frames(impath + "Slime_Jiggling.gif"),
    11: load_full_gif_frames(impath + "Slime_Jumping.gif"),
    12: load_full_gif_frames(impath + "Slime_Looking_Around.gif"),
    13: load_full_gif_frames(impath + "Slime_Open_Eye.gif"),
    14: load_full_gif_frames(impath + "Slime_Original.gif"),
    15: load_full_gif_frames(impath + "Slime_Sleeping.gif"),
}

# 通用播放函数
def play_animation(frames, on_start=None, on_end=None):
    cycle = 0

    if on_start:
        on_start()

    def update_frame(cycle):
        if cycle < len(frames):
            label.configure(image=frames[cycle])
            window.geometry(f"256x320+{x}+{y}")
            cycle += 1
            window.after(150, update_frame, cycle)
        else:
            if on_end:
                on_end()
            else:
                sleep_time = random.randint(3000, 7000)
                window.after(sleep_time, lambda: play_action_function(choose_action()))

    update_frame(cycle)

# 将每个动画封装为函数
def original_action():
    play_animation(animations[14], on_start=lambda: print("Original Action Start"))
    
def flying_action():
    global x, y

    # 备份原始位置
    original_x, original_y = x, y

    # 定义动画序列：(动画帧列表, on_start 回调)
    animation_sequence = [
        (animations[2], lambda: print("Flying Action Start - ON")),
        (animations[0], lambda: move_up()),
        (animations[0], lambda: move_down()),
        (animations[1], lambda: print("Flying Action Start - Off"))
    ]

    def play_next_animation(index=0):
        if index < len(animation_sequence):
            frames, on_start = animation_sequence[index]

            # 执行动画开始时的回调
            if on_start:
                on_start()

            # 播放当前动画
            play_animation(
                frames,
                on_end=lambda: play_next_animation(index + 1)
            )
        else:
            # 所有动画播放完毕，恢复原位
            global x, y
            x, y = original_x, original_y
            window.geometry(f"256x320+{x}+{y}")
            play_action_function(choose_action())

    def move_up(step=20, delay=75):
        global y
        if step > 0:
            y -= 10
            window.geometry(f"256x320+{x}+{y}")
            window.after(delay, move_up, step - 1, delay)

    def move_down(step=20, delay=75):
        global y
        if step > 0:
            y += 10
            window.geometry(f"256x320+{x}+{y}")
            window.after(delay, move_down, step - 1, delay)

    # 开始播放第一个动画
    play_next_animation()

def eating_action():
    # 定义目标路径变量
    target_delete_path = None

    # 函数定义放前面
    def try_eating():
        nonlocal target_delete_path
        deleted_path = ss.get_oldest_root_desktop_file(3)
        target_delete_path = deleted_path
        return bool(deleted_path)  # 返回 True/False 控制是否播放下个动画

    def eattinggggggggg():
        if not target_delete_path:
            print("Nothing to eat!")
            return
        xy.delete_directory_contents(target_delete_path)

    # 定义动画序列
    animation_sequence = [
        (animations[9], lambda: print("Hungry ...")),
        (animations[14], try_eating),
        (animations[7], eattinggggggggg),
        (animations[4], lambda: print("Yay"))
    ]

    # 动画播放逻辑
    def play_next_animation(index=0):
        if index >= len(animation_sequence):
            window.geometry(f"256x320+{x}+{y}")
            play_action_function(choose_action())
            return

        frames, on_start = animation_sequence[index]

        if on_start:
            result = on_start()
            if result is False:
                play_next_animation(index + 1)
                return

        play_animation(
            frames,
            on_end=lambda: play_next_animation(index + 1)
        )

    play_next_animation()
        
# 行动分类
special_actions = [2]
normal_actions = [0,1]

# 行动函数映射
action_functions = {
    0: original_action,
    1: flying_action,
    2: eating_action,
}

# 选择行动函数
def choose_action():
    global last_special_time
    current_time = time.time() * 1000
    if (current_time - last_special_time) >= cd_duration:
        action = random.choice(special_actions)
        last_special_time = current_time
        return action_functions[action]
    else:
        action = random.choice(normal_actions)
        return action_functions[action]

# 播放函数调用器
def play_action_function(action_function):
    action_function()

# 启动动画
label = tk.Label(window, bd=0, bg="black")
label.pack()

window.after(0, lambda: play_action_function(choose_action()))
window.mainloop()