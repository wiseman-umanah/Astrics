# script to handling all emailing and messaing to users and admins
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User


def notify_user_new_content(content_data):
	users  = User.objects.all()

	subject = "Wiseman from Astrics"

	for user in users:
		html_message  = render_to_string(
			'email/daily_update.html',
			{
				'content': content_data,
				'username': user.username
			}
		)
		email = EmailMessage(subject, html_message, to=[user.email])
		email.content_subtype = 'html'
		email.send()


def notify_admins(message):
	admins = User.objects.filter(is_admin=True).values_list('emails', flat=True)

	subject = "Wiseman from Astrics"
	html_message = render_to_string(
		'email/admin_failure.html',
		{
			'message': message
		}
	)
	email = EmailMessage(subject, html_message, to=admins)
	email.content_subtype = 'html'
	email.send()

