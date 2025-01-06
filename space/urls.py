from django.urls import path
from .views import ( Profile, post_list,
					follow_unfollow )


app_name  = 'space'

urlpatterns = [
	path('<str:username>', Profile.as_view(), name='profile'),
	path('<str:username>/posts/', post_list, name='posts'),
	path('<str:username>/relationship/', follow_unfollow, name='relationship'),
]
