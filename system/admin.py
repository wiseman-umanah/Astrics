from django.contrib import admin
from . models import AstricsModel


# Register your models here.
@admin.register(AstricsModel)
class AstricsAdmin(admin.ModelAdmin):
	fields = (
		"date", "title",
		"description","url",
		"media_type"
	)
	list_display = ['title', 'url', 'media_type', 'date']
