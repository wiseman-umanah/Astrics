from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from . forms import ( UserProfileEdit,
					 UserProfileForm,
					 UserPostForm,
					CommentForm )
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from account.models import ( Post, Like,
							UserProfile, Favorite )
from django.db.models import OuterRef, Exists
from django.core.paginator import ( Paginator,
								   EmptyPage,
								   PageNotAnInteger )
from system.models import AstricsModel
from account.forms import CustomPasswordForm
from django.contrib.postgres.search import SearchVector
from space.templatetags.space_extras import get_pic_link



@method_decorator(login_required, name='dispatch')
class Profile(View):
	template_name = 'space/profile.html'
	
	def get(self, request, username):
		user = get_object_or_404(User, username=username, is_active=True)

		form = UserProfileEdit(instance=user)  
		pic_form = UserProfileForm()
		password_form = CustomPasswordForm(user=user)
		
		posts = Post.objects.filter(user=user).annotate(
			is_liked=Exists(Like.objects.filter(
				post=OuterRef('pk'), user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user)))[:3]

		favorites = Favorite.objects.filter(
			user=user,
			post__media_type="image")[:5]
		
		return render(request, self.template_name, {
			'form': form,
			'pic_form': pic_form,
			'user_profile': user,
			'password_form': password_form,
			'posts': posts,
			'favorites': favorites
		})

	def post(self, request, username):
		user = get_object_or_404(User, username=username, is_active=True)

		form = UserProfileEdit(instance=user, data=request.POST)
		pic_form = UserProfileForm(data=request.POST, files=request.FILES)
		password_form = CustomPasswordForm(user=user, data=request.POST)

		posts = Post.objects.filter(user=user).annotate(
			is_liked=Exists(Like.objects.filter(
				post=OuterRef('pk'), user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user)))[:3]

		favorites = Favorite.objects.filter(
			user=user,
			post__media_type="image")[:5]
	
		if form.is_valid() and pic_form.is_valid() and password_form.is_valid():
			form.save()
			pic_form.save(request.user)
			password_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			print("form", form.errors)
			print("pic", pic_form.errors)
			print("passowrd", password_form.errors)
			messages.error(request, 'Error updating your profile')

		return render(request, self.template_name, {
			'form': form,
			'pic_form': pic_form,
			'password_form': password_form,
			'user_profile': user,
			'posts': posts,
			'favorites': favorites
		})




@login_required
@csrf_exempt
def user_posts(request, username):
	user = get_object_or_404(User, username=username)
	posts = Post.objects.filter(user=user).annotate(
			is_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user)))
	
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
	
	user_profile = get_object_or_404(UserProfile, user=request.user)
	
	action = request.GET.get('action').lower()

	if not action:
		return JsonResponse({'status': 'error',
					   'message': 'Missing action parameter'})

	if action not in ['unfollow', "follow"]:
		return JsonResponse({'status': 'error',
					   'message': 'Invalid action. Allowed action [unfollow, follow]'})
	
	if user_profile.user.username != username:
		if action == "unfollow":
			user_profile.follows.remove(other_user.profile)
		elif action == "follow":
			user_profile.follows.add(other_user.profile)
	
	return JsonResponse({'status': 'success', 'follows': other_user.profile.follows.count(),
											'followers': other_user.profile.followed_by.count()})


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
			return JsonResponse({"status": "unliked", "like_count": post.likes.count(), "comment_count": post.comments.count()})

		return JsonResponse({"status": "liked", "like_count": post.likes.count(), "comment_count": post.comments.count()})


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


@login_required
@csrf_exempt
def create_post(request):
	if request.method == "POST":
		form = UserPostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return JsonResponse({'message': 'Post successful'}, status=200)
		else:
			print('post form error', form.errors)
			return JsonResponse({'message': 'Invalid form parameters'}, status=400)


@login_required
@csrf_exempt
def create_comment(request, post_id):
	if request.method == "POST":
		try:
			post = get_object_or_404(Post, id=post_id)
		except Http404:
			return JsonResponse({'message': 'Post does not exist'}, status=404)

		form = CommentForm(request.POST)
		
		if form.is_valid():
			comment = form.save(commit=False)
			comment.user = request.user
			comment.post = post
			comment.save()
			return JsonResponse({'message': 'Comment successful'}, status=200)
		else:
			print('comment form error', form.errors)
			return JsonResponse({'message': 'Invalid form parameters'}, status=400)


@login_required
def get_post(request, username, post_id):
	user = get_object_or_404(User, username=username)
						
	main_userProfile = get_object_or_404(UserProfile, user=request.user)
	post_annotate = Post.objects.annotate(
		is_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user)))
	post = post_annotate.get(id=post_id, user=user)
	
	comments = post.comments.all()[:5]

	return render(request, 'posts/post.html', {'post': post,
											'section': 'home',
											'user': user,
											'main_userProfile': main_userProfile,
											'comments': comments})


@login_required
@csrf_exempt
def get_comments(request, username, post_id):
	user = get_object_or_404(User, username=username)

	post = Post.objects.get(id=post_id, user=user)
	paginator = Paginator(post.comments.all(), 5)
	page = request.GET.get('page')

	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = ""
	
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		return render(request, 'posts/comments.html', {'comments': comments})
	
	return render(request, 'posts/comments.html', {'comments': comments})


@login_required
def home(request):
	user = get_object_or_404(UserProfile, user=request.user)
	latest_post = AstricsModel.objects.first()
	posts = Post.objects.annotate(
		is_liked=Exists(Like.objects.filter(post=OuterRef('pk'),
									  user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user))).all()[:15]

	return render(request, 'space/home.html', {'user': user,
												'posts': posts,
												'section': 'home',
												'latest_post': latest_post})


@login_required
def get_allPosts(request):
	posts = Post.objects.annotate(
		is_liked=Exists(Like.objects.filter(post=OuterRef('pk'),
									  user=request.user))).annotate(
					in_favorite=Exists(Favorite.objects.filter(
						post=OuterRef('pk'), user=request.user))).all()
	paginator = Paginator(posts, 15)
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = ""
	
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		return render(request, 'posts/lists_posts.html', {'posts': posts})
	
	return render(request, 'posts/lists_posts.html', {'posts': posts})


def search(request):
	query = request.GET.get('query', '')
	
	if query:
		posts = Post.objects.annotate(search=SearchVector('title',)).filter(search=query)[:5]
		accounts = UserProfile.objects.annotate(search=SearchVector('user__username', 'user__first_name', 'user__last_name')).filter(search=query)[:3]

		results = {
			'posts': [{'title': post.title, 'url': post.get_absolute_url()} for post in posts],
			'accounts': [
				{
					'first_name': profile.user.first_name,
					'last_name': profile.user.last_name,
					'username': profile.user.username,
					'pic_url': get_pic_link(profile.user, 1),
					'url': profile.get_absolute_url()
				} for profile in accounts
			],
		}
	else:
		results = {'posts': [], 'accounts': []}

	return JsonResponse({'results': results})
