from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from . forms import CustomPasswordForm
from datetime import timedelta
from . models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from space.forms import UserPostForm



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

					return redirect('space:home')
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
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.email = user_form.clean_email()
			new_user.set_password(
				user_form.cleaned_data['password']
			)
			new_user.save()

			UserProfile.objects.create(user=new_user)
			return redirect('space:home')
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
		print("Form Errors:", form.errors)
		return self.render_to_response(self.get_context_data(form=form))


class CustomPasswordChangeView(PasswordChangeView):
	template_name = 'account/registration/password_change.html'
	
	def get_success_url(self):
		return reverse_lazy("space:user-profile", args=[self.request.user.username])

	def form_valid(self, password_form):
		password_form.save()

		update_session_auth_hash(self.request, password_form.user)
		return super().form_valid(password_form)

	def form_invalid(self, password_form):
		print("Form Errors:", password_form.errors)
		return self.render_to_response(self.get_context_data(password_form=password_form))


@method_decorator(login_required, name='dispatch')
class CreatePostView(FormView):
	template_name = 'post/post_form.html'
	form_class = UserPostForm

	def get_success_url(self):
		return reverse_lazy("profile", args=[self.request.user.username])
	
	def form_valid(self, post_form):
		post = post_form.save(commit=False)
		post.user = self.request.user
		post.save()

		return super().form_valid(post_form)

	def form_invalid(self, post_form):
		print("Form Errors:", post_form.errors)
		return self.render_to_response(self.get_context_data(post_form=post_form))
	
