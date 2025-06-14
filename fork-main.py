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
x = int(width * 0.3)
y = int(height * 0.75)

# 初始化参数
cd_duration = 500000 # 特殊行动共享CD（毫秒）
last_special_time = time.time() * 1000 - (cd_duration - 15000)  # 上次执行特殊行动的时间

# Tkinter窗口配置
window = tk.Tk()
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "black")
window.configure(bg='black')

# 自动调整函数
def adjust_location(x_input,y_input):
    global x, y
    adjust_width = 300
    adjust_height = 100
    extended_width = width + 150
    extended_height = height + 50
    if x_input < -150 -  adjust_width:
        x = x_input + extended_width + 50
    elif x_input > extended_width - adjust_width:
        x = x_input - extended_width
    else:
        x = x_input    
    
    y = y_input    


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
    8 : load_full_gif_frames(impath + "Slime_Go_Boom.gif"),
    9 : load_full_gif_frames(impath + "Slime_Hungry.gif"),
    10: load_full_gif_frames(impath + "Slime_Jiggling.gif"),
    11: load_full_gif_frames(impath + "Slime_Jumping.gif"),
    12: load_full_gif_frames(impath + "Slime_Looking_Around.gif"),
    13: load_full_gif_frames(impath + "Slime_Open_Eye.gif"),
    14: load_full_gif_frames(impath + "Slime_Original.gif"),
    15: load_full_gif_frames(impath + "Slime_Sleeping.gif"),
    100 : load_full_gif_frames(impath + "Slime_Balloon_Flying.gif", flip=True),
    101 : load_full_gif_frames(impath + "Slime_Balloon_Off.gif", flip=True),
    102 : load_full_gif_frames(impath + "Slime_Balloon_On.gif", flip=True),
    110: load_full_gif_frames(impath + "Slime_Jiggling.gif", flip=True),
    111: load_full_gif_frames(impath + "Slime_Jumping.gif", flip=True),
}

# 通用播放函数
def play_animation(frames, on_start=None, on_end=None):
    cycle = 0

    if on_start:
        on_start()

    def update_frame(cycle):
        if cycle < len(frames):
            label.configure(image=frames[cycle])
            window.geometry(f"512x320+{x}+{y}")
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
    def on_end():
        sleep_time = random.randint(100, 1000)
        window.after(sleep_time, lambda: play_action_function(choose_action()))
    play_animation(animations[14], on_start=lambda: print("Original Action Start"), on_end=on_end)
    
def blinking_action():
    def on_end():
        sleep_time = random.randint(1000, 2000)
        window.after(sleep_time, lambda: play_action_function(choose_action()))
    play_animation(animations[3], on_start=lambda: print("Blinking Action Start"), on_end=on_end)
    
def looking_arount_action():
    def on_end():
        sleep_time = random.randint(1000, 2000)
        window.after(sleep_time, lambda: play_action_function(choose_action()))

    play_animation(animations[12], on_start=lambda: print("Look arount Start"), on_end=on_end)

from PIL import ImageOps
import random

def jumping_action():
    global x

    # 随机决定跳跃方向
    direction = random.choice(["left", "right"])
    print(f"Jumping to the {direction}")


    # 翻转动画帧（如果需要）
    if direction == "right":
        # 加载翻转后的帧
        flipped_frames = animations[111]
        frames = flipped_frames
    else:
        frames = animations[11]

    move_step = 10  # 每帧移动像素数

    def update_position_and_animation(cycle=0):
        global x, y
        
        if cycle < len(frames):
            # 更新帧
            label.configure(image=frames[cycle])

            # 更新位置
            if direction == "left":
                target_x = x + move_step
                adjust_location(target_x, y)
            else:
                target_x = x - move_step
                adjust_location(x - move_step, y)

            window.geometry(f"512x320+{x}+{y}")

            # 播放下一帧
            window.after(150, update_position_and_animation, cycle + 1)
        else:
            # 动画结束，恢复原始位置
            window.geometry(f"512x320+{x}+{y}")
            play_action_function(choose_action())

    # 开始播放动画并同步移动
    update_position_and_animation()
    
def jiggling_action():
    global x

    # 随机决定弹射方向
    direction = random.choice(["left", "right"])
    print(f"Jiggling to the {direction}")

    # 翻转动画帧（如果需要）
    if direction == "right":
        # 加载翻转后的帧
        flipped_frames = animations[110]
        frames = flipped_frames
    else:
        frames = animations[10]

    move_step =10  # 每帧移动像素数

    def update_position_and_animation(cycle=0):
        global x

        if cycle < len(frames):
            # 更新帧
            label.configure(image=frames[cycle])

            # 更新位置
            if direction == "left":
                target_x = x + move_step
                adjust_location(target_x, y)
            else:
                target_x = x - move_step
                adjust_location(x - move_step, y)

            window.geometry(f"512x320+{x}+{y}")

            # 播放下一帧
            window.after(150, update_position_and_animation, cycle + 1)
        else:
            # 动画结束，恢复原始位置
            window.geometry(f"512x320+{x}+{y}")
            play_action_function(choose_action())

    # 开始播放动画并同步移动
    update_position_and_animation()
    
def flying_action():
    global x, y

    # 定义动画序列：(动画帧列表, on_start 回调)
    animation_sequence = []
    
    # 随机决定跳跃方向
    direction = random.choice(["left", "right"])
    print(f"Jiggling to the {direction}")

    # 翻转动画帧（如果需要）
    if direction == "right":
        animation_sequence = [
            (animations[102], lambda: print("Flying Action Start - ON")),
            (animations[100], lambda: move_up()),
            (animations[100], lambda: move_down()),
            (animations[101], lambda: print("Flying Action Start - Off"))
        ]
    else:
        animation_sequence = [
            (animations[2], lambda: print("Flying Action Start - ON")),
            (animations[0], lambda: move_up()),
            (animations[0], lambda: move_down()),
            (animations[0], lambda: 0),
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
            play_action_function(choose_action())

    def move_up(step=30, delay=75):
        global y,x
        if step > 0:
            random_offset = random.randint(3, 10)  # 随机偏移
            x_target = x
            if direction == "right":
                x_target = x - random_offset
            else:
                x_target = x + random_offset    
            y_target = y - 10
            adjust_location(x_target, y_target)
            window.geometry(f"512x320+{x}+{y}")
            window.after(delay, move_up, step - 1, delay)

    def move_down(step=30, delay=65):
        global y,x
        if step > 0:
            random_offset = random.randint(3, 10)  # 随机偏移
            x_target = x
            if direction == "right":
                x_target = x - random_offset
            else:
                x_target = x + random_offset    
            y_target = y + 10
            adjust_location(x_target, y_target)
            window.geometry(f"512x320+{x}+{y}")
            window.after(delay, move_down, step - 1, delay)

    # 开始播放第一个动画
    play_next_animation()

def sleep_action():

    # 定义动画序列：(动画帧列表, on_start 回调)
    animation_sequence = [
        (animations[5], lambda: print("sleeping Action Start - Close zzz")),
        (animations[15], lambda: print("Sleep")),
        (animations[15], lambda: print("Sleep")),
        (animations[13], lambda: print("Wake up"))
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
            play_action_function(choose_action())

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
            window.geometry(f"512x320+{x}+{y}")
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
normal_actions = [0,1,3,4,5,6,7]

# 行动函数映射
action_functions = {
    0: original_action,
    1: flying_action,
    2: eating_action,
    3: blinking_action,
    4: sleep_action,
    5: looking_arount_action,
    6: jumping_action,
    7: jiggling_action,
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