import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

def send_email(subject, body, to_email):
    try:
        from_email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        host_server = os.getenv("EMAIL_HOST", "smtp.163.com")
        port = 465
        
        if not from_email or not password:
            raise ValueError("Email credentials not set in environment variables.")
        
        # 设置邮件内容
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(host_server, port)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        
        print(f"Email sent to {to_email} successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 示例调用
if __name__ == "__main__":
    to_email = os.getenv('RECIPIENT_EMAIL')
    subject = "Stock Alert"
    body = "Your stock alert notification message."
    
    send_email(subject, body, to_email)