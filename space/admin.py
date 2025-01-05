from django.contrib import admin
from . models import FileModel
from account.models import Post
from space.forms import UserPostForm

# Register your models here.

@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
	readonly_fields = ('hash', 'file_id',)
	fields = ('file_id', 'hash', 'reference_count')
	list_display = ('file_id', 'reference_count')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	form = UserPostForm
	readonly_fields = ('file_id',)

	fields = (
		'user', 'title',
		'description', 'media_file', 'file_id',
		'media_type',)

	list_display = ('id', 'title', 'file_id', 'media_type', 'user',)
	search_fields = ('user', 'title', )

	class Meta:
		ordering = ['-created_at']
	