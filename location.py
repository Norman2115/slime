import pyautogui
import cv2
import numpy as np
import time
import os
import platform
import subprocess

def open_folder_containing_file(folder_path):
    """Opens Finder (macOS) or File Explorer (Windows) for the given folder."""
    print(f"📂 Opening folder: {folder_path}")
    system = platform.system()

    if system == "Windows":
        # Windows: Open folder in File Explorer
        subprocess.run(["explorer", folder_path])
    elif system == "Darwin":
        # macOS: Open folder in Finder
        subprocess.run(["open", folder_path])
    else:
        print("Unsupported OS. Proceeding without opening folder...")

def locate_file_on_screen(target_filename, threshold=0.6):
    """
    Locate a file icon with given filename on screen using template matching.
    Returns (x, y) center position if found, None otherwise.
    """

    print("📸 Taking screenshot...")
    # Take full screen screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    print(f"📄 Preparing template for '{target_filename}'...")

    # Create blank image for template
    font = cv2.FONT_HERSHEY_SIMPLEX
    template_size = (300, 40)  # Width x Height
    template = np.zeros(template_size[::-1], dtype=np.uint8)

    # Draw text on template
    cv2.putText(template, target_filename, (5, 30), font, 1, (255, 255, 255), 2)

    # Match template
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    # Get all matches
    matches = list(zip(*loc[::-1]))  # Convert to (x, y)

    if matches:
        print(f"✅ Found '{target_filename}' at {len(matches)} location(s).")
        x, y = matches[0]  # Use first match
        center_x = x + template_size[0] // 2
        center_y = y + template_size[1] // 2
        print(f"🎯 Center position: ({center_x}, {center_y})")
        return center_x, center_y
    else:
        print("❌ File not found on screen.")
        return None


# === Main Execution ===
if __name__ == "__main__":
    # 📝 Replace these with your actual file and folder path
    filename_to_find = "example.txt"
    folder_path = "C:\\Users\\user\\Desktop"  # or "C:\\Users\\yourusername\\Documents" on Windows

    print(f"🚀 Opening folder containing '{filename_to_find}'...")
    open_folder_containing_file(filename_to_find, folder_path)

    print(f"⏱️  Waiting 5 seconds for Finder/File Explorer to appear...")
    time.sleep(5)  # Give Finder/File Explorer time to open

    position = locate_file_on_screen(filename_to_find)

    if position:
        x, y = position
        print(f"\n🎉 Final screen coordinates: x={x}, y={y}")
        # You can now move your desktop pet here
        # Example: move_pet_to(x, y)
    else:
        print("\n⚠️ Could not locate file on screen.")