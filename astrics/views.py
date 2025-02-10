from django.shortcuts import render



def landing_page(request):
	return render(request, 'account/landing-page.html')
