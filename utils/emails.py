# script to handling all emailing and messaing to users and admins
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import random


email_subjects = [
    "New Space Content: Explore the Latest Discovery",
    "Unveiling New Space Content: What’s Out There?",
    "Discover New Space Content: Insights and Innovations",
    "New Space Content Alert: Don’t Miss Out!",
    "Dive into New Space Content: Expanding Our Universe",
    "New Space Content: Fascinating Facts and Figures",
    "Get Excited for New Space Content: Upcoming Releases",
    "New Space Content: Join the Journey Beyond Earth"
]


def notify_user_new_content(content_data):
	users  = User.objects.all()

	subject = random.choice(email_subjects)

	for user in users:
		html_message  = render_to_string(
			'emails/daily_update.html',
			{
				'content': content_data,
				'username': user.username
			}
		)
		email = EmailMessage(subject, html_message, to=[user.email])
		email.content_subtype = 'html'
		email.send()


def notify_admins(message):
	admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)

	subject = "Important Notice"
	html_message = render_to_string(
		'emails/admin_failure.html',
		{
			'message': message
		}
	)
	email = EmailMessage(subject, html_message, to=admins)
	email.content_subtype = 'html'
	email.send()

