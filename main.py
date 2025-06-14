import tkinter as tk
import random

# Initial state
x = 1400
y = 800
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
slime_original = [tk.PhotoImage(file=impath + "Slime_Original.gif", format="gif -index 0")]
slime_jiggling = [tk.PhotoImage(file=impath + "Slime_Jiggling.gif", format="gif -index %i" % i) for i in range(7)]
slime_looking = [tk.PhotoImage(file=impath + "Slime_Looking_Around.gif", format="gif -index %i" % i) for i in range(9)]
slime_blinking = [tk.PhotoImage(file=impath + "Slime_Blinking.gif", format="gif -index %i" % i) for i in range(12)]

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
