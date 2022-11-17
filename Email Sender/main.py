from email.message import EmailMessage
import ssl
import smtplib

# your email address
email_sender = ''
# your 2-factor app password for your email account
email_password = ''
# receiver's email address
email_receiver = ''

subject = "Email from the Python Email Sender"
body = """
Code Hard, Play hard!
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())