import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
import django
django.setup()




import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.models import Settings



# Your Gmail account credentials
def send_email(subject,html):
    settings=Settings.objects.get()
    gmail_user =settings.email
    gmail_password = settings.password  # Use your App Password if you have 2FA enabled

    # Email details
    reciever_email = settings.reciever_email
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

html="<p>test</p>"

send_email('test',html)