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


def send_email(image_link):	
	msg_text = """
				Hello World, We are glad that this message reached you.
				 
				It's a new day with a beautiful view of the space around.
				This message is delivered to you because of your spevial interest in space, we love you and wish you a good health
				
				%s
				
				Astrics Corp.""" % (image_link)

	msg_html = '''<html><head></head><body><h1>Hello World!!</h1>
				<p>We are glad that this message reached you. ☺
				 
				It\'s a new day with a beautiful view of the space around.
				This message is delivered to you because of your spevial interest in space, we love you and wish you a good health
				
				🚀</p>
				<img src="%s"/><h3>Astrics Corp</h3></body></html>''' % (image_link)

	
	with smtplib.SMTP(gmail_server, gmail_port) as server:
		server.starttls()
		server.login(my_email, password_key)
		
		msg = MIMEMultipart()
		msg["Subject"] = "Astrics Daily Astronomical Pictures"
		msg["From"] = formataddr(("Explore Your Space", f"{my_email}"))
		msg["To"] = my_email
		msg.preamble = "Daily Update from Astrics"

		msg_alt = MIMEMultipart('alternative')
		msg.attach(msg_alt)
		msg_alt.attach(MIMEText(msg_text))
		msg_alt.attach(MIMEText(msg_html, 'html'))

		server.sendmail(my_email, users + [my_email], msg.as_string())
