from django.contrib import admin
from . models import UserProfile
from space.models import FileModel
from django.forms import forms
from space.forms import AdminUserProfileForm
from utils.files import ( upload_file_to_appwrite,
						 cleanup_unnecessary_file,
						 calculate_file_hash )



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = AdminUserProfileForm
    readonly_fields = ('profile_pic_id', 'cover_pic_id')

    def save_model(self, request, obj, form, change):
        if 'profile_pic' in form.cleaned_data and form.cleaned_data['profile_pic']:
            profile_pic = form.cleaned_data['profile_pic']
            if profile_pic.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Profile Image must be less than 10MB.")

            file_hash = calculate_file_hash(profile_pic)
            existing_file = FileModel.objects.filter(hash=file_hash).first()

            if existing_file:
                existing_file.reference_count += 1
                existing_file.save()
                obj.profile_pic_id = existing_file.file_id
            else:
                profile_pic.seek(0)
                file_id = upload_file_to_appwrite(profile_pic.read(), filename=profile_pic.name)
                obj.profile_pic_id = file_id
                FileModel.objects.create(hash=file_hash, file_id=file_id, reference_count=1)

        if 'cover_pic' in form.cleaned_data and form.cleaned_data['cover_pic']:
            cover_pic = form.cleaned_data['cover_pic']
            if cover_pic.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Cover Image must be less than 10MB.")

            file_hash = calculate_file_hash(cover_pic)
            existing_file = FileModel.objects.filter(hash=file_hash).first()

            if existing_file:
                existing_file.reference_count += 1
                existing_file.save()
                obj.cover_pic_id = existing_file.file_id
            else:
                cover_pic.seek(0)
                file_id = upload_file_to_appwrite(cover_pic.read(), filename=cover_pic.name)
                obj.cover_pic_id = file_id
                FileModel.objects.create(hash=file_hash, file_id=file_id, reference_count=1)

        super().save_model(request, obj, form, change)
