from django.contrib import admin
from . models import FileModel


# Register your models here.
@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
	fields = ('file_id', 'hash', 'reference_count')
	list_display = ('file_id', 'reference_count')
	