#!/usr/bin/python3
import smtplib
from os import getenv
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()

my_email = getenv("EMAIL")
password_key = getenv("PWD_KEY")

# SMTP Server and port no for GMAIL.com
gmail_server= "smtp.gmail.com"
gmail_port= 587


def send_email(subject, receiver_email):
	msg = EmailMessage()
	msg["Subject"] = subject
	msg["From"] = formataddr(("Coding is Fun Corp", f"{my_email}"))
	msg["To"] = receiver_email
	msg["BCC"] = my_email
	
	msg.set_content("Hello World, if you recieve this it's for testing purpose")

	with smtplib.SMTP(gmail_server, gmail_port) as server:
		server.starttls()
		server.login(my_email, password_key)
		server.sendmail(my_email, receiver_email, msg.as_string())

if __name__ == "__main__":
	send_email(
		subject="Testing",
		receiver_email="rjijoe@gmail.com"
	)
