import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email, password, array, dataset):
    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # 收件人邮箱
    msg['Subject'] = fr'{dataset} Number of submissions'
    
    # 邮件正文
    string = ''.join([str(element) for element in array])
    text = MIMEText(string)
    msg.attach(text)
     
    # 发送邮件
    try:
        smtp = smtplib.SMTP('smtp.126.com')  # 使用 smtp.126.com
        smtp.login(email, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败，错误信息：', e)

if __name__ == '__main__':
    # 直接硬编码邮箱账号和密码
    myemail = "lllaaaiaccept_666@126.com"  # 填入你的邮箱
    password = "KSh7d68NK3Nz8Rg9"  # 填入你的邮箱密码

    array = [0 for x in range(1)]
    send_email(myemail, password, array, 'cremad')
