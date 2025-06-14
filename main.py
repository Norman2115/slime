import tkinter as tk
import random

# Initial state
x = 1400
cycle = 0
check = 0
event_number = random.choice([0, 1, 2, 3])

# Path to GIFs (make sure they are in this folder)
impath = "assets/"

# Create Tkinter window
window = tk.Tk()
window.overrideredirect(True)               # remove window border
window.wm_attributes("-topmost", True)      # keep slime on top
window.configure(bg='black')                # fallback background (won't be seen with transparent gifs)
# window.wm_attributes("-transparentcolor", "black")  # only if you use black-background gifs

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
    window.geometry(f"100x100+{x}+1050")

    # Move to next frame
    cycle += 1
    if cycle >= len(frames):
        cycle = 0
        event_number = random.choice(list(animations.keys()))  # pick a new action

    window.after(150, update, cycle, event_number, x)

# Start the loop
window.after(0, update, cycle, event_number, x)
window.mainloop()
