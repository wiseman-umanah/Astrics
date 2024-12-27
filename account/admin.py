from django.contrib import admin
from space.forms import UserProfileForm
from . models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
	form = UserProfileForm
