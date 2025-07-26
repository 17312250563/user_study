import os

root = r"C:\Users\12551\Desktop\user_study\camn" # 替换成你的目录

for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if fname.startswith("gesturelsm_") and fname.endswith(".mp4"):
            # 生成新文件名
            new_fname = fname.replace("gesturelsm_", "camn_", 1)
            old_path = os.path.join(dirpath, fname)
            new_path = os.path.join(dirpath, new_fname)
            os.rename(old_path, new_path)
            print(f"重命名: {old_path} -> {new_path}")
