# import os

# root = r"C:\Users\12551\Desktop\user_study"
# methods = ["ours", "camn", "gesturelsm", "DiffuseStyle", "zeroggs"]

# # 获取所有方法下的case子文件夹集合
# case_sets = []
# for method in methods:
#     sub_path = os.path.join(root, method)
#     if not os.path.exists(sub_path):
#         print(f"方法文件夹不存在: {sub_path}")
#         continue
#     cases = [d for d in os.listdir(sub_path) if os.path.isdir(os.path.join(sub_path, d))]
#     case_sets.append(set(cases))

# # 取交集，保证五个方法都齐全
# valid_cases = set.intersection(*case_sets)
# print(f"五方法都齐全的动作组(case)数: {len(valid_cases)}")

# group_count = 0

# with open("filenames.txt", "w", encoding='utf-8') as f:
#     for case in sorted(valid_cases):
#         group_ok = True
#         for method in methods:
#             sub_dir = os.path.join(root, method, case)
#             mp4s = [file for file in os.listdir(sub_dir)
#                     if file.endswith('.mp4') and file.startswith(method+"_")]
#             if mp4s:
#                 f.write(os.path.join(sub_dir, mp4s[0]) + "\n")
#             else:
#                 f.write(f"缺少:{os.path.join(sub_dir, method+'_XX_YY.mp4')}\n")
#                 group_ok = False
#         f.write("\n")  # 组间空行
#         if group_ok:
#             group_count += 1

# print(f"实际可用完整分组: {group_count} 组")




# import os
# from collections import defaultdict

# # 读取原文件
# with open("C:\\Users\\12551\\Desktop\\src\\filenames.txt", "r", encoding='utf-8') as fin:
#     lines = [line.strip() for line in fin if line.strip()]
# groups = defaultdict(dict)
# method_names = []

# for path in lines:
#     parts = path.replace("\\", "/").split('/')
#     if len(parts) < 4:
#         continue
#     method = parts[-3]
#     case = parts[-2]
#     fname = parts[-1]
#     if method not in method_names:
#         method_names.append(method)
#     case_id = case  # 以case文件夹名为一组
#     groups[case_id][method] = path

# # 输出分组数量
# print(f"共 {len(groups)} 组（case）")

# # 如果还要输出每组case的名字，可以加：
# print("组名示例：", list(groups.keys())[:5])
import os
from collections import defaultdict

root = r"C:\Users\12551\Desktop\src\video"
project_root = r"C:\Users\12551\Desktop\src"  # 项目根目录，用于计算相对路径
    
methods = ["emage", "gesturelsm", "zeroeggs", "diffuseStyle", "ours"]

# 获取所有方法下的case集合（交集）
case_sets = []
for method in methods:
    cases = [d for d in os.listdir(os.path.join(root, method))
             if os.path.isdir(os.path.join(root, method, d))]
    case_sets.append(set(cases))
valid_cases = set.intersection(*case_sets)

group_count = 0

with open("filenames.txt", "w", encoding='utf-8') as f:
    for case in sorted(valid_cases):
        # 收集每个方法下所有mp4，按后缀分组
        suffix2path = defaultdict(dict)
        for method in methods:
            case_dir = os.path.join(root, method, case)
            for file in os.listdir(case_dir):
                if file.endswith('.mp4') and file.startswith(method + "_"):
                    # 提取时间段后缀（如_0_10.mp4）
                    suffix = file[len(method):]  # _0_10.mp4
                    abs_path = os.path.abspath(os.path.join(case_dir, file))
                    rel_path = os.path.relpath(abs_path, project_root)
                    suffix2path[suffix][method] = rel_path
        # 只输出五方法都齐全的时间段
        for suffix in sorted(suffix2path):
            files = suffix2path[suffix]
            if all(m in files for m in methods):
                for m in methods:
                    f.write(files[m] + '\n')
                f.write('\n')
                group_count += 1
            else:
                lost = [m for m in methods if m not in files]
                print(f"缺少:{case} {suffix} -> {lost}")

print(f"可用完整分组(五方法同时间段)共: {group_count} 组")


# import os

# root = r"C:\Users\12551\Desktop\src\video"
# methods = ["ours", "camn", "gesturelsm", "DiffuseStyle", "zeroggs"]

# with open("filenames.txt", "w", encoding="utf-8") as f:
#     for method in methods:
#         method_dir = os.path.join(root, method)
#         for case in os.listdir(method_dir):
#             subdir = os.path.join(method_dir, case)
#             if os.path.isdir(subdir):
#                 for mp4 in os.listdir(subdir):
#                     if mp4.endswith('.mp4') and mp4.startswith(method + "_"):
#                         abs_path = os.path.abspath(os.path.join(subdir, mp4))
#                         f.write(abs_path + "\n")
