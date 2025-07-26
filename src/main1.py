import streamlit as st
import random

# ------------------ 方法标签、基本参数 ------------------
method_labels = ["emage", "gesturelsm", "zeroggs", "DiffuseStyle", "ours"]
method_num = 5     # 每组5个方法
group_num = 40     # 总共40组动作（即有200个视频）
video_num = 2      # 每人只做两组（10个视频）
max_participants = 1  # 限制最大参与人数

# ------------------ 初始化参与人数计数器 ------------------
if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = False

if "participant_count" not in st.session_state:
    st.session_state["participant_count"] = 0

# ------------------ 如果已提交结果，则不再加载内容 ------------------
if st.session_state["participant_count"] >= max_participants and not st.session_state["button_clicked"]:
    st.warning("参与人数已达上限，感谢您的关注！")
    st.stop()

# ------------------ 读取所有视频路径 ------------------
with open("filenames.txt", "r", encoding='utf-8') as f:
    file_list = [line.strip() for line in f if line.strip()]

# --------- 初始化分组，每组5个视频，二维存储 ----------
if "user_group_file_list" not in st.session_state:
    all_group_indices = list(range(group_num))
    selected_groups = random.sample(all_group_indices, video_num)
    group_file_list = []
    for g in selected_groups:
        start = g * method_num
        group_file_list.append(file_list[start : start + method_num])
    st.session_state["user_group_file_list"] = group_file_list
    st.session_state["group_numbers"] = [g + 1 for g in selected_groups]
    st.session_state["human_likeness"] = [None for _ in range(video_num * method_num)]
    st.session_state["speech_appropriateness"] = [None for _ in range(video_num * method_num)]
    st.session_state["style_appropriateness"] = [None for _ in range(video_num * method_num)]
    st.session_state["page_num"] = 1

user_group_file_list = st.session_state["user_group_file_list"]
group_numbers = st.session_state["group_numbers"]
human_likeness = st.session_state["human_likeness"]
speech_appropriateness = st.session_state["speech_appropriateness"]
style_appropriateness = st.session_state["style_appropriateness"]

# ------------------ 说明 ------------------
def instrunction():
    st.header("Instructions: ")
    st.markdown("请仔细阅读以下对本研究的介绍，您需要在生成的人体运动之间进行评分：")
    st.markdown("##### 1. 运动真实性评分")
    st.markdown("请观察视频中虚拟角色的运动，并判断其是否符合人类的真实行为习惯。（请忽略面部表情）")
    st.markdown("##### 2. 运动与音频一致性评分")
    st.markdown("请评估视频中的运动与音频的节奏是否一致。（请忽略面部表情）")
    st.markdown("##### 3. 运动风格准确度评分")
    st.markdown("观察虚拟角色的运动风格是否一致。（请忽略面部表情）")
    st.markdown("###### 注意：本实验专注于身体运动，不关注面部表情。")

# ------------------ 每页评分 ------------------
def QA(page_idx):
    group_files = user_group_file_list[page_idx - 1]
    base = (page_idx - 1) * method_num

    for i in range(method_num):
        video_path = group_files[i]
        print(f"Processing video: {video_path}")
        method_name = method_labels[i]

        # st.markdown(f"**{method_name}**")
        with open(video_path, 'rb') as vf:
            st.video(vf.read())

        col1, col2, col3 = st.columns(3)
        with col1:
            human_likeness[base + i] = st.feedback("stars", key=f"hl_{page_idx}_{i}")
            st.caption('真实性')
        with col2:
            speech_appropriateness[base + i] = st.feedback("stars", key=f"sp_{page_idx}_{i}")
            st.caption('音频一致性')
        with col3:
            style_appropriateness[base + i] = st.feedback("stars", key=f"st_{page_idx}_{i}")
            st.caption('风格准确度')
        st.markdown("---")

    if (None in human_likeness[base:base+method_num] or
        None in speech_appropriateness[base:base+method_num] or
        None in style_appropriateness[base:base+method_num]):
        return False
    return True

# ------------------ 主逻辑 ------------------
def main():
    instrunction()
    num = st.session_state["page_num"]
    # st.subheader(f"动作组 {num} / {video_num}（你本次需要评价的组编号：{group_numbers}）")
    st.write("每组有 5 个视频，请为每个视频打分（1~5 星）。")

    res = QA(num)

    if num == 1:
        if st.button("下一组"):
            if res:
                st.session_state["page_num"] += 1
                st.rerun()
            else:
                st.warning("请完成本组所有评分后再进入下一组。")
    elif num == video_num:
        col1, col2 = st.columns(2)
        if not st.session_state["button_clicked"]:
            if col1.button("提交结果"):
                if not res:
                    st.warning("请完成所有评分！")
                else:
                    # 提交后计入参与人数
                    count = read_email_(myemail, password)
                    count += 1
                    send_email(myemail, password, count)
                    ID, localtime = data_collection(myemail, password, human_likeness, speech_appropriateness, style_appropriateness, count)
                    st.divider()
                    st.session_state["button_clicked"] = True
                    st.markdown(':blue[请对下面的评分结果截图保存。]')
                    st.write("**动作组编号**: ", group_numbers)
                    st.write("human_likeness: ", human_likeness)
                    st.write("speech_appropriateness: ", speech_appropriateness)
                    st.write("style_appropriateness: ", style_appropriateness)
        if st.session_state["button_clicked"]:
            st.success("结果提交成功！感谢您的参与！")
        if col2.button("上一组"):
            st.session_state["page_num"] -= 1
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        if col1.button("上一组"):
            st.session_state["page_num"] -= 1
            st.rerun()
        if col2.button("下一组"):
            if res:
                st.session_state["page_num"] += 1
                st.rerun()
            else:
                st.warning("请完成本组所有评分后再进入下一组。")

# ------------------ 启动 ------------------
if __name__ == '__main__':
    st.set_page_config(page_title="userstudy", layout="wide")
    myemail = st.secrets["my_email"]["email"]  
    password = st.secrets["my_email"]["password"]
    dataset = "ablation"

    count = read_email(myemail, password)
    if count>=60: 
        st.error("答题人数已满，感谢你的理解！")
        st.cache_data.clear()
    else:
        main()
