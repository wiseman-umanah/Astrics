#!/usr/bin/python3
import smtplib
from os import getenv
# from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from backend.models import storage
from backend.models.user import User
from email.mime.multipart import MIMEMultipart

load_dotenv()

my_email = getenv("EMAIL")
password_key = getenv("PWD_KEY")

# SMTP Server and port no for GMAIL.com
gmail_server= "smtp.gmail.com"
gmail_port= 587

users = storage.all(User).values()
users = [(x.to_dict())["email"] for x in users]


def send_email(image_link, description, title):	
	msg_text = """%s
				%s 
				%s
				
				Astrics Space.""" % (title, description, image_link)

	msg_html = '''<html><head></head><body><h1>%s</h1>
				<p>%s</p>
				<img src="%s"/>
				<h3>Astrics Space</h3></body></html>''' % (title, description, image_link)

	
	with smtplib.SMTP(gmail_server, gmail_port) as server:
		server.starttls()
		server.login(my_email, password_key)
		
		msg = MIMEMultipart()
		msg["Subject"] = "Picture Of The Day"
		msg["From"] = formataddr(("Sunday Space Talk 😁️", f"{my_email}"))
		msg["To"] = my_email
		msg.preamble = "Served from Astrics"

		msg_alt = MIMEMultipart('alternative')
		msg.attach(msg_alt)
		msg_alt.attach(MIMEText(msg_text))
		msg_alt.attach(MIMEText(msg_html, 'html'))

		server.sendmail(my_email, users + [my_email], msg.as_string())
