import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


# tuple([last subject sent]:[last time sent])
db = []

SUPRESSION_INTERVAL = os.getenv("SUPRESSION_INTERVAL", 60 * 10) # units: second


def send_email(subject, body, to_email):
    # check suppression
    datetime_now = datetime.now()
    for _, (last_subject, last_time) in enumerate(db):
        if subject == last_subject and datetime_now - last_time < timedelta(seconds=SUPRESSION_INTERVAL):
            print(f"Email suppressed for subject: {subject}")
            return

    try:
        from_email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        host_server = os.getenv("EMAIL_HOST", "smtp.163.com")
        port = 465

        if not from_email or not password:
            raise ValueError("Email credentials not set in environment variables.")

        # 设置邮件内容
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # 连接 SMTP 服务器并发送邮件
        server = smtplib.SMTP_SSL(host_server, port)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email} successfully.")
        datetime_now = datetime.now()
        for subject, _ in db:
            if subject == subject:
                db.remove((subject, _))
                break
        db.append((subject, datetime_now))
    except Exception as e:
        print(f"Failed to send email: {e}")


# 示例调用
if __name__ == "__main__":
    to_email = os.getenv("RECIPIENT_EMAIL")
    subject = "Stock Alert"
    body = "Your stock alert notification message."

    send_email(subject, body, to_email)
