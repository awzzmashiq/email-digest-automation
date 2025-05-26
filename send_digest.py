import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(digest):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Daily Email Digest"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    part1 = MIMEText(digest, "plain")
    msg.attach(part1)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
