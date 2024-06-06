import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_code(email):
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your_email@gmail.com"
    smtp_password = "your_app_password"
    
    # Konfigurasi email server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = email
    message['Subject'] = "Email Verification Code"
    
    body = f"Your verification code is {verification_code}"
    message.attach(MIMEText(body, 'plain'))
    
    # Kirim email
    server.send_message(message)
    server.quit()
    
    return verification_code
