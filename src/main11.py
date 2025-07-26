import streamlit as st
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import poplib
from email.parser import Parser
import json
import random

#按照5个视频一组读取
def load_video_groups(filename="filenames.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        assert len(lines) % 5 == 0, "视频总数应为5的倍数"
        groups = [lines[i:i+5] for i in range(0, len(lines), 5)]  # 40组，每组5条
    return groups  # List[List[str]]

#读取邮件内容
def get_group_assign_counts(email, password, dataset_prefix):
    counts = [0] * 40  # 初始每组0人
    try:
        server = poplib.POP3_SSL('pop.126.com', 995)
        server.user(email)
        server.pass_(password)
        _, total, _ = server.list()

        for i in range(len(total), 0, -1):  # 从最近的邮件向前
            try:
                raw_email = b"\n".join(server.retr(i)[1]).decode("utf-8", errors="ignore")
                message = Parser().parsestr(raw_email)
                subject = message["Subject"]
                if not subject.startswith(dataset_prefix):
                    continue
                # 抓取正文内容
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(part.get_content_charset())
                        try:
                            data = json.loads(body)
                            if isinstance(data, dict) and "assigned_groups" in data:
                                for g in data["assigned_groups"]:
                                    counts[g] += 1
                        except Exception:
                            continue
                        break
            except Exception:
                continue
        server.quit()
    except Exception as e:
        print("读取邮箱失败：", e)
    return counts  # 长度40，每组的使用次数


#分配当前用户的2个可用组
def assign_2_groups(counts, max_per_group=3):
    available = [i for i, c in enumerate(counts) if c < max_per_group]
    if len(available) < 2:
        return None
    return random.sample(available, 2)

#组装视频路径供页面使用
def flatten_video_paths(groups, assigned_indices):
    return [vid for idx in assigned_indices for vid in groups[idx]]

@st.cache_data
def send_email(email, password, array):
    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = fr'{dataset} Number of submissions'
    
    # 邮件正文
    #string = ''.join([str(element) for element in array])
    string = str(array)
    text = MIMEText(string)
    msg.attach(text)
     
    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

@st.cache_data
def read_email(myemail, password):
    try:
        pop3_server = 'pop.126.com'
        subject_to_search = f'{dataset} Number of submissions'
        print(f"[Debug] 尝试连接 {pop3_server}，账户：{myemail}")

        # 连接到 POP3 服务器
        mail_server = poplib.POP3_SSL(pop3_server, 995)
        print("[Debug] 成功建立 POP3 SSL 连接")
        mail_server.user(myemail)
        mail_server.pass_(password)
        print("[Debug] 登录成功")

        # 搜索符合特定主题的邮件
        num_messages = len(mail_server.list()[1])
        print(f"[Debug] 邮箱中总共有 {num_messages} 封邮件")
        content = None  # 初始化变量
        found = False
        for i in range(num_messages, 0, -1):
            raw_email = b'\n'.join(mail_server.retr(i)[1]).decode('utf-8')
            email_message = Parser().parsestr(raw_email)
            subject = email_message['Subject']
            
            if subject == subject_to_search:
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode(part.get_content_charset())
                        found = True
                        break  # 找到满足条件的邮件后及时跳出循环
                if found:
                    break

        # 关闭连接
        mail_server.quit()
         # ✅ 如果找不到内容，说明还没有人提交，返回 0
        if content is None:
            return 0
        array = [int(char) for char in content]
        result = int("".join(map(str, array)))
        return result

    except Exception as e:
        st.error('')

@st.cache_data
def read_email_(myemail, password):
    try:
        pop3_server = 'pop.126.com'
        subject_to_search = f'{dataset} Number of submissions'

        # 连接到 POP3 服务器
        mail_server = poplib.POP3_SSL(pop3_server, 995)
        mail_server.user(myemail)
        mail_server.pass_(password)

        # 搜索符合特定主题的邮件
        num_messages = len(mail_server.list()[1])
        content = None  # 初始化变量
        found = False
        for i in range(num_messages, 0, -1):
            raw_email = b'\n'.join(mail_server.retr(i)[1]).decode('utf-8')
            email_message = Parser().parsestr(raw_email)
            subject = email_message['Subject']
            
            if subject == subject_to_search:
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode(part.get_content_charset())
                        found = True
                        break  # 找到满足条件的邮件后及时跳出循环
                if found:
                    break

        # 关闭连接
        mail_server.quit()
        array = [int(char) for char in content]
        result = int("".join(map(str, array)))
        return result

    except Exception as e:
        st.error('')

@st.cache_data
def data_collection(email, password, human_likeness, smoothness, semantic_accuracy, count):
    # 发送内容
    # 新增：从 session 中获取用户分配的组号
    assigned_groups = st.session_state.get("group_indices", [])
    # 打包正文内容（转成 JSON 形式）
    content_dict = {
        "assigned_groups": assigned_groups,
        "human_likeness": human_likeness,
        "smoothness": smoothness,
        "semantic_accuracy": semantic_accuracy
    }
    # data1 = ''.join(str(x) for x in human_likeness)
    # data2 = ''.join(str(x) for x in smoothness)
    # data3 = ''.join(str(x) for x in semantic_accuracy)
    # string = data1 + "\n" + data2 + "\n" + data3
    string = json.dumps(content_dict, ensure_ascii=False, indent=2)
    localtime = datetime.strptime(time.strftime('%m-%d %H-%M-%S', time.localtime()), '%m-%d %H-%M-%S')
    localtime += timedelta(hours=8)
    seconds = localtime.strftime('%S')
    localtime = localtime.strftime('%m-%d %H-%M-%S')
    # 打开文件并指定写模式
    ID = f"{count}-{seconds}"
    file_name = dataset + ' ' + str(count) + ' ' + localtime + ".txt"
    file = open(file_name, "w")
    # 将字符串写入文件
    file.write(string)
    # 关闭文件
    file.close()

    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = dataset + ' ' + str(count) + ' '  + localtime

    # 邮件正文
    text = MIMEText(string)
    msg.attach(text)

    # 添加附件
    with open(file_name, 'rb') as f:
        attachment = MIMEApplication(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(attachment)

    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

    return ID, localtime

@st.cache_data
def instrunction():
    st.header("Instructions: ")
    st.markdown('''请仔细阅读以下对本研究的介绍，您需要在生成的人体运动之间进行评分：''')
    st.markdown('''##### 1. 运动真实性评分''')
    st.markdown('''请观察视频中虚拟角色的运动，并判断其是否符合人类的真实行为习惯（请忽略面部表情）。
- 关注运动的真实感。''')
    st.markdown('''##### 2. 运动与音频一致性评分''')
    st.markdown('''请评估视频中的运动与音频的节奏是否一致（请忽略面部表情）。
- 注意观察动作是否随着语音节奏自然起伏，是否有突然加速或延迟的情况；
- 评判动作与语音中的停顿、重音、语气变化是否协调；''')
    st.markdown('''##### 3. 运动风格准确度评分''')
    st.markdown('''观察左边虚拟角色的运动风格是否与右边的参考视频中虚拟人的运动风格一致（请忽略面部表情）。
- 风格可包含肢体动作的速度、幅度、节奏感；
- 注意角色整体运动是否有类似的张力、流畅度或表现力；
- 不要求动作一模一样，但整体风格应具有可感知的一致性。''')
    st.markdown('''###### 注意事项：本实验专注于身体运动，不需要关注面部表情。''')
    st.markdown('''###### 手机端用户可以在手机横屏状态下答题，如遇卡顿和视频播放不了的情况，建议在电脑端答题。''')

def QA(human_likeness, speech_appropriateness, style_appropriateness, num, method_num):
    start = group_index * method_num  # 起始下标
    end = start + method_num          # 结束下标
    all_filled = True


    for i in range(start, end):
        st.markdown(f"**第 {i - start + 1} 个视频评分：**")

        col1, col2, col3 = st.columns(3)
        with col1:
            human_likeness[i] = st.radio(
                f"真实性评分",
                [1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"human_{i}"
            )
        with col2:
            speech_appropriateness[i] = st.radio(
                f"运动与音频一致性评分",
                [1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"speech_{i}"
            )
        with col3:
            style_appropriateness[i] = st.radio(
                f"风格准确度评分",
                [1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"style_{i}"
            )
        st.divider()
        if (human_likeness[i] is None or
            speech_appropriateness[i] is None or
            style_appropriateness[i] is None):
            all_filled = False
    
    return all_filled  
def QA_group(human_likeness, speech_appropriateness, style_appropriateness, group_index, method_num):
    start = group_index * method_num  # 起始下标
    end = start + method_num          # 结束下标
    all_filled = True

    for i in range(start, end):
        st.markdown(f"**第 {i - start + 1} 个视频评分：**")

        col1, col2, col3 = st.columns(3)
        with col1:
            human_likeness[i] = st.radio(
                f"真实性评分",
                [1, 2, 3, 4, 5],
                index=0,
                horizontal=True,
                key=f"human_{i}"
            )
        with col2:
            speech_appropriateness[i] = st.radio(
                f"运动与音频一致性评分",
                [1, 2, 3, 4, 5],
                index=0,
                horizontal=True,
                key=f"speech_{i}"
            )
        with col3:
            style_appropriateness[i] = st.radio(
                f"风格准确度评分",
                [1, 2, 3, 4, 5],
                index=0,
                horizontal=True,
                key=f"style_{i}"
            )

        st.divider()

        if (human_likeness[i] is None or
            speech_appropriateness[i] is None or
            style_appropriateness[i] is None):
            all_filled = False

    return all_filled

def QA_group_separated(human_likeness, speech_appropriateness, style_appropriateness, group_index, method_num, video_list):
    start = group_index * method_num
    end = start + method_num
    all_filled = True

    for i in range(start, end):
        st.markdown(f"### 视频 {i - start + 1}")
        video_path = video_list[i]
        print(f"[Debug] 播放视频 {video_path}")
        st.video(video_path)

        col1, col2, col3 = st.columns(3)
        with col1:
            human_likeness[i] = st.radio(
                "真实性评分",
                [1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"human_{i}"
            )
        with col2:
            speech_appropriateness[i] = st.radio(
                "运动与音频一致性评分",
                [1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"speech_{i}"
            )
        with col3:
            style_appropriateness[i] = st.radio(
                "风格准确度评分",
                [1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"style_{i}"
            )

        st.divider()

        if (human_likeness[i] is None or
            speech_appropriateness[i] is None or
            style_appropriateness[i] is None):
            all_filled = False

    return all_filled

@st.cache_data
def play_video(file_path):
    return file_path

def page(video_num, method_num):
    instrunction()


    def switch_page(page_num):
        st.session_state["page_num"] = page_num
        st.session_state["human_likeness"] = human_likeness 
        st.session_state["speech_appropriateness"] = speech_appropriateness 
        st.session_state["style_appropriateness"] = style_appropriateness
        st.rerun()  # 清空页面

    # 通过 st.session_state 实现页面跳转
    if "page_num" not in st.session_state:
        st.session_state["page_num"] = 1

    num = st.session_state["page_num"]

    # st.subheader(fr"Video {num} / {video_num}")
    #st.write(file_list[num-1].rstrip())
    video_list = st.session_state["video_list"]
    group_index = num - 1  # 第 num 页代表的是第几个组（从 0 开始）
    st.subheader(fr"第 {num} 页 / 共 {video_num} 页")
    st.write("本页共包含 5 个视频，请分别对其打分。")

    start = group_index * method_num
    end = start + method_num
    # # 展示本页的5个视频
    # for i in range(start, end):
    #     st.markdown(f"**视频 {i - start + 1}:**")
    #     video_bytes = play_video(video_list[i])
    #     st.video(video_bytes)

    # 展示评分项
    res = QA_group_separated(human_likeness, speech_appropriateness, style_appropriateness, group_index, method_num, video_list)
    # 第1页
    if st.session_state["page_num"] == 1:
        if st.button("下一页"):
            if res:
                switch_page(st.session_state["page_num"] + 1)
            else:
                st.warning("请回答当前页问题！")

    # 中间页
    if num > 1 and num < video_num:
        col1, col2 = st.columns(2)
        if col2.button("上一页"):
            switch_page(st.session_state["page_num"] - 1)
        if col1.button("下一页"):
            if res:
                switch_page(st.session_state["page_num"] + 1)
            else:
                st.warning("请回答当前页问题！")

    # 最后一页
    if st.session_state["page_num"] == video_num:
        col1, col2 = st.columns(2)
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False

        if not st.session_state.button_clicked:
            if col1.button("提交结果"):
                if not res:
                    st.warning("请回答当前页问题！")
                else:
                    st.write('提交中...请耐心等待...')
                    count = read_email_(myemail, password)
                    if count is None:
                        # st.warning("⚠️ 无法从邮箱读取已有提交数，初始化为 0")
                        count = 0
                    count += 1
                    
                    
                    send_email(myemail, password, count)


                    try:
                        ID, localtime = data_collection(myemail, password, human_likeness, speech_appropriateness, style_appropriateness, count)
                        st.success("📎 带评分结果的邮件发送成功")
                    except Exception as e:
                        st.error(f"❌ data_collection 邮件发送失败: {e}")
                        st.stop()
                    st.divider()
                    st.markdown(':blue[请对下面的结果进行截图。]')
                    st.write("**Result:**")
                    st.write("human_likeness: ", str(human_likeness))
                    st.write("speech_appropriateness: ", str(speech_appropriateness))
                    st.write("style_appropriateness: ", str(style_appropriateness))
                    st.write("**提交时间:** ", localtime)
                    st.write("**提交ID:** ", ID)
                    st.session_state.button_clicked = True 

        if st.session_state.button_clicked == True:
            st.cache_data.clear()
            st.success("Successfully submitted the results. Thank you for using it. Now you can exit the system.")

        if col2.button("上一页"):
            switch_page(st.session_state["page_num"] - 1)


if __name__ == '__main__':
    st.set_page_config(page_title="userstudy")
    #st.cache_data.clear() # 初始化
    myemail = "lllaaaiaccept_666@126.com"  # 填入你的邮箱
    password = "KSh7d68NK3Nz8Rg9"  # 填入你的邮箱密码


    dataset = "ablation"

    count = read_email(myemail, password)

    if count>=60: 
        st.error("答题人数已满，感谢你的理解！")
        st.cache_data.clear()
    else:
            # ------------------- 视频组分配逻辑（插入部分） -------------------
        if "video_list" not in st.session_state:
            groups = load_video_groups()
            counts = get_group_assign_counts(myemail, password, dataset)

            assigned = assign_2_groups(counts)
            if not assigned:
                st.error("当前所有组已被分配完")
                st.stop()

            video_list = flatten_video_paths(groups, assigned)

            st.session_state["video_list"] = video_list
            st.session_state["group_indices"] = assigned
            st.session_state["video_num"] = 2  # 保存到 session
            st.session_state["method_num"] = 5  # 保存到 session    
        # ✅ 不管是不是新用户，都取出 video_num/method_num
        video_num = st.session_state["video_num"]
        method_num = st.session_state["method_num"]

        if "human_likeness" and "speech_appropriateness" and "style_appropriateness" not in st.session_state:
            human_likeness = [1 for x in range(video_num*method_num)]
            speech_appropriateness = [1 for x in range(video_num*method_num)]
            style_appropriateness = [1 for x in range(video_num*method_num)]
        else:
            human_likeness = st.session_state["human_likeness"]
            speech_appropriateness = st.session_state["speech_appropriateness"]
            style_appropriateness = st.session_state["style_appropriateness"]

        page(video_num, method_num)
