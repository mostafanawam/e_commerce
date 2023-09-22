# tasks.py (inside one of your Django apps)
from celery import shared_task
from time import sleep

import logging

logger = logging.getLogger(__name__)



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings.models import Settings





@shared_task()  
def send_email(subject,html,reciever_email):
    settings=Settings.objects.get()
    gmail_user =settings.email
    gmail_password = settings.password  # Use your App Password if you have 2FA enabled

    # Email details
    subject = subject

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = reciever_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html, "html"))

    email_string = msg.as_string()

    # Connect to Gmail's SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Enable TLS (Transport Layer Security)
        
        # Log in to your Gmail account
        server.login(gmail_user, gmail_password)
        
        # Send the email
        server.sendmail(gmail_user,reciever_email,email_string)

    print('Email sent successfully!')

