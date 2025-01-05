from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . forms import UserProfileEdit, UserProfileForm, UserPostForm
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class Profile(View):
	template_name = 'space/profile.html'
	
	def get(self, request, username):
		user = get_object_or_404(User, username=username, is_active=True)

		form = UserProfileEdit(instance=user)  
		pic_form = UserProfileForm()
		post_form = UserPostForm()

		return render(request, self.template_name, {
			'form': form,
			'pic_form': pic_form,
			'post_form': post_form,
			'user_profile': user
		})

	def post(self, request, username):
		user = get_object_or_404(User, username=username, is_active=True)

		form = UserProfileEdit(instance=user, data=request.POST)
		pic_form = UserProfileForm(data=request.POST, files=request.FILES)
		post_form = UserPostForm(data=request.POST, files=request.FILES)


		if form.is_valid() and pic_form.is_valid():
			form.save()
			pic_form.save(request.user)
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')

		if post_form.is_valid():
			post = post_form.save(commit=False)
			post.user = request.user
			post.save()
			messages.success(request, 'Post created successfully')
		else:
			messages.error(request, 'Error creating new post')

		return render(request, self.template_name, {
			'form': form,
			'pic_form': pic_form,
			'post_form': post_form,
			'user_profile': user
		})
