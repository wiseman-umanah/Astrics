from django.contrib.auth.models import User
from django import forms
from account.models import UserProfile
from . models import FileModel
from utils.files import ( upload_file_to_appwrite,
						 cleanup_unnecessary_file,
						 calculate_file_hash )



class UserProfileEdit(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs.update({
			'placeholder': "Edit your firstname",
		})
		self.fields['last_name'].widget.attrs.update({
			'placeholder': "Edit your lastname",
		})
		self.fields['email'].widget.attrs.update({
			'placeholder': "Edit your email",
			'required': 'True',
		})
		self.fields['username'].widget.attrs.update({
			'placeholder': "Edit your spacename",
			'required': 'True',
		})



class UserProfileForm(forms.Form):
	profile_pic = forms.ImageField(
		widget=forms.FileInput(attrs={
			'id': 'id_profile_pic',
			'style': 'display: none;',
		}), 
		required=False
	)
	cover_pic = forms.ImageField(
		widget=forms.FileInput(attrs={
			'id': 'id_cover_pic',
			'style': 'display: none;',
		}), 
		required=False
	)

	def save(self, user):
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		
		if profile_pic:= self.cleaned_data.get('profile_pic'):
			if profile_pic.size > 10 * 1024 * 1024:
				raise forms.ValidationError("Image must be less than 10MB.")
			file_hash = calculate_file_hash(profile_pic)

			existing_file = FileModel.objects.filter(hash=file_hash).first()
			if existing_file:
				existing_file.reference_count += 1
				existing_file.save()
				user_profile.profile_pic_id = existing_file.file_id
			else:
				profile_pic.seek(0)
				file_id = upload_file_to_appwrite(profile_pic.read(), filename=profile_pic.name)
				user_profile.profile_pic_id = file_id
		
		if cover_pic:= self.cleaned_data.get('cover_pic'):
			if cover_pic.size > 10 * 1024 * 1024:
				raise forms.ValidationError("Image must be less than 10MB.")
			file_hash = calculate_file_hash(cover_pic)

			existing_file = FileModel.objects.filter(hash=file_hash).first()
			if existing_file:
				existing_file.reference_count += 1
				existing_file.save()
				user_profile.cover_pic_id = existing_file.file_id
			else:
				cover_pic.seek(0)
				file_id = upload_file_to_appwrite(cover_pic.read(), filename=cover_pic.name)
				user_profile.cover_pic_id = file_id
		

		user_profile.save()
		return user_profile
