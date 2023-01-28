from core.settings import EMAIL_INFO

# Email
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient:
    port = 465
    smtp_server = "smtp.gmail.com"

    def __init__(self):
        self.sender = EMAIL_INFO['sender']
        self.password = EMAIL_INFO['password']

    def send_email(self, receiver: str, subject: str, html: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = receiver
        html_mime = MIMEText(html, "html")
        message.attach(html_mime)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EmailClient.smtp_server, EmailClient.port, context=context) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, receiver, message.as_string())
