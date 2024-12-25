from django.urls import path
from .views import Profile

urlpatterns = [
	path('<str:username>', Profile.as_view(), name='profile'),
]
