import os

def list_videos_in_subfolders_to_txt(parent_folder, output_file, video_extensions=(".mp4", ".avi", ".mov", ".mkv")):
    with open(output_file, "w", encoding="utf-8") as f:
        for folder_name in os.listdir(parent_folder):
            folder_path = os.path.join(parent_folder, folder_name)
            if os.path.isdir(folder_path):
                f.write(f"📁 文件夹: {folder_name}\n")
                video_files = [
                    file for file in os.listdir(folder_path)
                    if file.lower().endswith(video_extensions)
                ]
                if video_files:
                    for video in video_files:
                        full_path = os.path.join(folder_path, video)
                        if video.startswith("res_"):
                            try:
                                os.remove(full_path)
                                print(f"🗑️ 已删除: {full_path}")
                            except Exception as e:
                                print(f"❌ 删除失败: {full_path}, 原因: {e}")
                                continue
                        else:
                            f.write(f"  🎬 视频: {video}\n")
                else:
                    f.write("  ⚠️ 没有视频文件\n")
                f.write("\n")  # 空行分隔不同文件夹

    print(f"✅ 视频列表已保存到: {output_file}")

if __name__ == "__main__":
    base_path = r"C:\Users\12551\Desktop\user_study\video\ours"  # 📌 修改为你的路径
    output_path = os.path.join(base_path, "video_list.txt")
    list_videos_in_subfolders_to_txt(base_path, output_path)
