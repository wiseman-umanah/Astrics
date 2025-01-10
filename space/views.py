from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from . forms import ( UserProfileEdit,
					 UserProfileForm,
					 UserPostForm )
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from account.models import ( Post, Like,
							Comment, Favorite )
from django.db.models import OuterRef, Exists
from django.core.paginator import ( Paginator,
								   EmptyPage,
								   PageNotAnInteger )



@method_decorator(login_required, name='dispatch')
class Profile(View):
	template_name = 'space/profile.html'
	
	def get(self, request, username):
		user = get_object_or_404(User, username=username, is_active=True)

		form = UserProfileEdit(instance=user)  
		pic_form = UserProfileForm()
		post_form = UserPostForm()
		
		posts = Post.objects.filter(user=user).annotate(
			is_liked=Exists(Like.objects.filter(
				post=OuterRef('pk'), user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user)))[:3]

		return render(request, self.template_name, {
			'form': form,
			'pic_form': pic_form,
			'post_form': post_form,
			'user_profile': user,
			'posts': posts
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




@login_required
def post_list(request, username):
	user = get_object_or_404(User, username=username)
	posts = Post.objects.filter(user=user).annotate(
			is_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=request.user)))
	
	paginator = Paginator(posts, 4)
	page = request.GET.get('page')
	
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = ""
	
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		return render(request, 'posts/list_posts.html', {'posts': posts})
	
	return render(request, 'posts/list_posts.html', {'posts': posts})


@login_required
def follow_unfollow(request, username):
	try:
		other_user = get_object_or_404(User, username=username)
	except Http404:
		return JsonResponse({'status': 'error',
					   'message': 'The user to be followed does not exist'})
	
	user = request.user
	
	action = request.GET.get('action').lower()

	if not action:
		return JsonResponse({'status': 'error',
					   'message': 'Missing action parameter'})

	if action not in ['unfollow', "follow"]:
		return JsonResponse({'status': 'error',
					   'message': 'Invalid action. Allowed action [unfollow, follow]'})
	
	if user.username != username:
		if action == "unfollow":
			user.profile.follows.remove(other_user.profile)
		elif action == "follow":
			user.profile.follows.add(other_user.profile)
	
	return JsonResponse({'status': 'success'})


@login_required
@csrf_exempt
def like_unlike(request, post_id):
	if request.method == "POST":
		try:
			post = Post.objects.get(id=post_id)
		except Http404:
			return JsonResponse({'status': 'error',
						'message': f'The Post with id {post_id} with does not Exist'})

		like, created = Like.objects.get_or_create(user=request.user, post=post)

		if not created:
			like.delete()
			return JsonResponse({"status": "unliked", "like_count": post.likes.count()})

		return JsonResponse({"status": "liked", "like_count": post.likes.count()})


@login_required
@csrf_exempt
def save_remove_favorite(request, post_id):
	if request.method == "POST":
		try:
			post = Post.objects.get(id=post_id)
		except Http404:
			return JsonResponse({'status': 'error',
						'message': f'The Post with id {post_id} with does not Exist'})

	fav, created = Favorite.objects.get_or_create(user=request.user, post=post)

	if not created:
		fav.delete()
		return JsonResponse({'status': 'removed', "message": "Post removed from favorite"})

	return JsonResponse({'status': 'added', "message": "Post added to your favorite"})
