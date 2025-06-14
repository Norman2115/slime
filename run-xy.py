import xy
import ss
# if __name__ == "__main__":
#     target_dir = input("请输入要删除的目录路径：").strip()
#     xy.delete_directory_contents(target_dir)

# if __name__ == "__main__":
#     print(ss.get_oldest_old_desktop_file(3))

target_file = ss.get_oldest_old_desktop_file(3)
# target_file = "target1.txt"
print(f"Target file: {target_file}")
if target_file:
    print(xy.get_desktop_icon_position(target_file))