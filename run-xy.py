import xy

if __name__ == "__main__":
    target_dir = input("请输入要删除的目录路径：").strip()
    xy.delete_directory_contents(target_dir)