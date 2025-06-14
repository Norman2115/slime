import random
import tkinter as tk
import pyautogui

x = 1400
cycle = 0
check = 1
idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]
event_number = random.randrange(1,3,1)
impath = "assets/"


# Tkinter window to place our pet
window = tk.Tk()

idle = [tk.PhotoImage(file=impath + "idle.gif", format="gif -index %i" % i) for i in range(9)] # idle gif, 9 frames


label = tk.Label(window, bd=0)
label.pack()
window.mainloop()


# Since we call our .gif in the form of array, we need to make a function to loop each frame
# Everytime we call this function, the variable cycle will increase by 1.
# When it is big enough, it will change the event_number to a random number, because
# we want the pet change it actions every time the .gif have looped once.
def gif_work(cycle, frames, event_number, first_num, last_num):
  if cycle < len(frames) - 1:
    cycle += 1
  else:
    cycle = 0
    event_number = random.randrange(first_num, last_num + 1, 1)
  return cycle, event_number


# Update the frame

