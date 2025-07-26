import streamlit as st
import os
import poplib
from email import policy
from email.parser import BytesParser

def download_txt_attachment_pop3(myemail, password, dataset, save_path='./'):
    try:
        # POP3 服务器地址和端口
        pop3_server = 'pop.126.com'
        subject_to_search = f'{dataset}'  # 以 dataset 开头的邮件主题
        stop_subject = 'ablation 2 06-17 17-13-15'  # 设置停止条件的邮件标题

        # 连接到 POP3 服务器
        mail_server = poplib.POP3_SSL(pop3_server, 995)
        mail_server.user(myemail)
        mail_server.pass_(password)

        # 获取邮件数量
        num_messages = len(mail_server.list()[1])
        print(f'总共有 {num_messages} 封邮件')

        for i in range(num_messages, 0, -1):  # 从最新的邮件开始遍历
            # 获取邮件的原始内容
            raw_email = b'\n'.join(mail_server.retr(i)[1])
            
            # 解析邮件
            email_message = BytesParser(policy=policy.default).parsebytes(raw_email)

            # 获取邮件主题
            subject = email_message['Subject']

            if subject and subject == stop_subject:
                print(f'找到特定邮件：{subject}，停止遍历')
                break

            # 如果邮件主题符合搜索条件，继续原有的保存操作
            if subject and subject.startswith(subject_to_search):  # 检查邮件主题
                print(f'找到符合条件的邮件：{subject}')
                if subject == 'comparsion Number of submissions': continue

                # 构建文件路径，文件名为邮件标题，替换无效字符
                filename = f"{subject.replace('/', '_').replace('\\', '_')}.txt"
                filename = ' '.join(filename.split()[:2])
                filepath = os.path.join(save_path, filename + '.txt')
                if(os.path.exists(filepath)): 
                    print(f'文件 {filename} 已存在，跳过')
                    continue

                # 提取邮件正文
                for part in email_message.walk():
                    # 处理 text/plain 类型的正文
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')

                        # 将正文写入本地文件
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(body)
                        print(f'邮件正文已保存为 {filepath}')
                        break  # 保存第一个符合条件的部分后跳出循环

        # 关闭与邮件服务器的连接
        mail_server.quit()

    except Exception as e:
        print(f'发生错误: {str(e)}')

# 获取 Streamlit 秘钥
myemail = st.secrets["my_email"]["email"]  
password = st.secrets["my_email"]["password"]

# 设置数据集和保存路径
type = ["ablation"]
for dataset in type:
    title = dataset 
    save_path = f'./result/{dataset}'
    os.makedirs(save_path, exist_ok=True)
    download_txt_attachment_pop3(myemail, password, title, save_path=save_path)
