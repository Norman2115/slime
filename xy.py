import os
import shutil
import stat

def delete_directory_contents(target_path):
    """
    Delete the target directory and all its subdirectories and files. Yummy ψ(・ω´・,,ψ

    Parameters:
    target_dir (str): the directory path to be deleted

    Return:
    Bool: True if deletion was successful, False otherwise
    """
    if not os.path.exists(target_path):
            print(f"Warning: {target_path} does not exist, nothing to delete.")
            return False

    try:
        if os.path.isfile(target_path) or os.path.islink(target_path):
            # 删除文件或符号链接
            os.remove(target_path)
            print(f"Successfully deleted file: {target_path}")
            return True

        elif os.path.isdir(target_path):
            # 删除目录及其内容
            def on_rm_error(func, path, exc_info):
                # 修改只读文件权限后重试
                os.chmod(path, stat.S_IWRITE)
                func(path)

            shutil.rmtree(target_path, onerror=on_rm_error)
            print(f"Successfully deleted directory: {target_path}")
            return True

        else:
            print(f"Unknown type of path: {target_path}")
            return False

    except Exception as e:
        print(f"Error deleting {target_path}: {str(e)}")
        return False
