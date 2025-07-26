import os

def write_filenames_to_txt(folder_path, output_txt_path):
    with open(output_txt_path, 'w') as f:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                # 将文件名逐行写入 txt 文件
                f.write(f"{folder_path}/" + f"{filename}\n")
    print(f"文件名已写入 {output_txt_path}")

# 输入文件夹路径和输出 txt 文件路径
folder_path = 'video'
output_txt_path = 'filenames.txt'

# 执行写入操作
write_filenames_to_txt(folder_path, output_txt_path)
