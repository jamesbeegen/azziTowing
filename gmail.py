from __future__ import print_function
import os.path
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv

try:
    load_dotenv()
except:
    pass

# CONFIG VARIABLES
PORT = 465  # For SSL
SERVER = "smtp.gmail.com"
SENDER = os.environ['admin_email']  # Enter your address
PASSWORD = os.environ['admin_email_password']


# Send payment link to client
def send_payment_link_via_email(client_email, name, link):
    msg = EmailMessage()
    msg.set_content("""
<p>Hi, {}! Thanks for choosing Azzi Towing. Please use the link below to pay for your service.</p>
<br>
<a href="{}">Click here to pay</a>
<p></p>
<br>
Thank you!
<br>
Joe Azzi
<br>
Owner,
<br>
Azzi Towing LLC""".format(name, link), 'html')
    msg['Subject'] = 'Azzi Towing: Invoice'
    msg['From'] = SENDER
    msg['To'] = client_email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg, from_addr=SENDER, to_addrs=client_email)


# Sends temporary password to the admin email - password reset/change
def send_temp_password(password):
    msg = EmailMessage()
    msg.set_content("""
<p>Temporary login password:</p>
<br>
<p>{}</p>
<br>
<p>You can change your password to a permanent password after logging in with the temporary password</p>""".format(password), 'html')
    msg['Subject'] = 'Temporary Password'
    msg['From'] = SENDER
    msg['To'] = SENDER
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg, from_addr=SENDER, to_addrs=SENDER)


# Sends an email after a customer schedules a service through the web form
def send_request_recieved_email(client_email, name, date, service_type, time_window):
    msg = EmailMessage()
    msg.set_content("""
<p>{}, we have received your service request.</p>
<h4>Service request details:</h4>
<p style="font-weight: bold;">Type: <span style="font-weight: normal;">{}</span></p>
<p style="font-weight: bold;">Date: <span style="font-weight: normal;">{}</span></p>
<p style="font-weight: bold;">Time: <span style="font-weight: normal;">{}</span></p>
<br>
<p> We will send another email when the service is confirmed. Thank you!</p>""".format(name, service_type, date, time_window), 'html')
    msg['Subject'] = 'Your Service Request Has Been Received'
    msg['From'] = SENDER
    msg['To'] = client_email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg, from_addr=SENDER, to_addrs=client_email)


# Sends a confirmation after service approval
def send_service_confirmation_email(client_email, name, date, service_type, time_window):
    msg = EmailMessage()
    msg.set_content("""
<p>{}, your service has been approved and confirmed.</p>
<br>
<h3>Confirmed service details:</h3>
<p style="font-weight: bold;">Type: <span style="font-weight: normal;">{}</span></p>
<p style="font-weight: bold;">Date: <span style="font-weight: normal;">{}</span></p>
<p style="font-weight: bold;">Time: <span style="font-weight: normal;">{}</span></p>
<br>
<p>We look forward to seeing you!</p>""".format(name, service_type, date, time_window), 'html')
    msg['Subject'] = 'Service Confirmation'
    msg['From'] = SENDER
    msg['To'] = client_email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg, from_addr=SENDER, to_addrs=client_email)