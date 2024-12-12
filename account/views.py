from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import PasswordResetConfirmView
from . forms import CustomPasswordForm
from datetime import timedelta



def user_login(request):
	if request.method == 'POST':
		remember = request.POST.get('remember')

		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'],
								password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					messages.success(request, 'Login successful!')

					if remember:
						request.session.set_expiry(timedelta(days=30))
					else:
						request.session.set_expiry(0)

					return HttpResponse('This is ok')
				else:
					messages.error(request, 'Your account is disabled.')
			else:
				messages.error(request, 'Invalid username or password.')
	else:
		form = LoginForm()
	return render(request, 'account/registration/login.html', {'form': form})


def user_registration(request):
	if request.method == 'POST':
		user_form = RegisterForm(request.POST)
		print(dir(user_form))
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.email = user_form.clean_email()
			new_user.set_password(
				user_form.cleaned_data['password']
			)
			new_user.save()
			return HttpResponse('Account successfully created')
	else:
		user_form = RegisterForm()
	return render(request,
			   'account/registration/register.html',
			   {'form': user_form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordForm

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Log form errors to help with debugging
        print("Form Errors:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

