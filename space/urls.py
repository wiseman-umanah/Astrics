from django.urls import path
from . import views


app_name  = 'space'

urlpatterns = [
	path('<str:username>', views.Profile.as_view(), name='profile'),
	path('<str:username>/posts/', views.post_list, name='posts'),
	path('<str:username>/relationship/', views.follow_unfollow, name='relationship'),
	path('create_post/', views.create_post, name='create_post'),
	path('post/<int:post_id>/like/', views.like_unlike, name='like-post'),
	path('post/<int:post_id>/save/', views.save_remove_favorite, name='save_remove'),
	path('post/<int:post_id>/create_comment', views.create_comment, name="create_comment"),
]
