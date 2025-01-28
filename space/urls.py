from django.urls import path
from . import views


app_name  = 'space'

urlpatterns = [
	path('', views.home, name='home'),
	path('search/', views.search, name='search'),
	path('posts/', views.get_allPosts, name='posts'),
	path('<str:username>', views.Profile.as_view(), name='user-profile'),
	path('<str:username>/posts/', views.user_posts, name='user-posts'),
	path('<str:username>/relationship/', views.follow_unfollow, name='user-relationship'),
	path('create_post/', views.create_post, name='create_post'),
	path('<str:username>/post/<int:post_id>', views.get_post, name='view-post'),
	path('<str:username>/post/<int:post_id>/comments', views.get_comments, name='view-comments'),
	path('post/<int:post_id>/like/', views.like_unlike, name='like-post'),
	path('post/<int:post_id>/save/', views.save_remove_favorite, name='save_remove'),
	path('post/<int:post_id>/create_comment', views.create_comment, name="create_comment"),
]
