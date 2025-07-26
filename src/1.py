# import os
# import subprocess

# # 指定顶层视频目录（所有方法目录如 camn/ours/... 都在这个下面）
# VIDEO_ROOT = r"C:\Users\12551\Desktop\src\video"
# ffmpeg_path = r"C:\Users\12551\scoop\shims\ffmpeg.exe"  # FFmpeg 路径

# # 递归遍历所有子目录中的 .mp4 文件
# for root, dirs, files in os.walk(VIDEO_ROOT):
#     for filename in files:
#         if filename.endswith(".mp4") and "_compatible" not in filename:
#             input_file = os.path.join(root, filename)
#             output_file = os.path.join(root, f"{os.path.splitext(filename)[0]}_compatible.mp4")

#             command = [
#                 ffmpeg_path,
#                 "-i", input_file,
#                 "-c:v", "libx264",
#                 "-c:a", "aac",
#                 "-pix_fmt", "yuv420p",
#                 "-movflags", "+faststart",
#                 output_file
#             ]

#             print(f"开始转码: {input_file}")
#             result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#             if result.returncode == 0:
#                 print(f"✅ 转码成功: {output_file}")
#             else:
#                 print(f"❌ 转码失败: {input_file}\n错误信息:\n{result.stderr.decode('utf-8')}")

# import os

# # 视频文件根目录
# VIDEO_ROOT = r"C:\Users\12551\Desktop\src\video"

# # 遍历所有子目录并删除非 compatible 的 .mp4 文件
# deleted_files = []

# for root, dirs, files in os.walk(VIDEO_ROOT):
#     for file in files:
#         if file.endswith(".mp4") and "_compatible" not in file:
#             full_path = os.path.join(root, file)
#             try:
#                 os.remove(full_path)
#                 deleted_files.append(full_path)
#                 print(f"🗑️ 已删除: {full_path}")
#             except Exception as e:
#                 print(f"❌ 删除失败: {full_path}，原因: {e}")

# print(f"\n✅ 共删除 {len(deleted_files)} 个非兼容视频文件")

import os

# 视频文件根目录
VIDEO_ROOT = r"C:\Users\12551\Desktop\src\video"

# 遍历所有子文件夹并重命名 *_compatible.mp4 -> *.mp4
renamed_files = []

for root, dirs, files in os.walk(VIDEO_ROOT):
    for file in files:
        if file.endswith("_compatible.mp4"):
            old_path = os.path.join(root, file)
            new_filename = file.replace("_compatible", "")
            new_path = os.path.join(root, new_filename)

            try:
                os.rename(old_path, new_path)
                renamed_files.append((old_path, new_path))
                print(f"✅ 重命名: {old_path} → {new_path}")
            except Exception as e:
                print(f"❌ 重命名失败: {old_path}，原因: {e}")

print(f"\n共重命名 {len(renamed_files)} 个视频文件")
