from django.shortcuts import render
from system.models import AstricsModel


def landing_page(request):
	latest_post = AstricsModel.objects.first()
	return render(request, 'account/landing-page.html',
			   {
				   'latest_post': latest_post
			   })
