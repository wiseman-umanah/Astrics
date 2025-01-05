from django.urls import path
from .views import Profile, post_list


app_name  = 'space'

urlpatterns = [
	path('<str:username>', Profile.as_view(), name='profile'),
	path('<str:username>/posts/', post_list, name='posts'),
]
