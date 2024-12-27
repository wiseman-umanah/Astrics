from django.contrib.auth.models import User
from django import forms
from account.models import UserProfile
from . models import FileModel
from utils.utils import ( upload_file_to_appwrite,
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



class UserProfileForm(forms.ModelForm):
	profile_pic_id = forms.CharField( 
		required=False, 
		widget=forms.TextInput(attrs={
			'readonly': 'readonly', 
		})
	)
	
	cover_pic_id = forms.CharField(
		required=False, 
		widget=forms.TextInput(attrs={
			'readonly': 'readonly', 
		})
	)

	profile_pic = forms.ImageField(widget=forms.FileInput(
		attrs= { 'id': 'id_profile_pic',
		  		'style': 'display: none;',
		  }), required=False)
	cover_pic = forms.ImageField(widget=forms.FileInput(
		attrs= { 'id': 'id_cover_pic',
		  		'style': 'display: none;',
		  }), required=False)

	class Meta:
		model = UserProfile
		fields = ('profile_pic', 'cover_pic')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance:
			self.fields['profile_pic_id'].initial = self.instance.profile_pic
			self.fields['cover_pic_id'].initial = self.instance.cover_pic

	def save(self, commit=True):
		user_profile = super().save(commit=False)

		if profile_pic:=self.cleaned_data['profile_pic']:
			if hasattr(profile_pic, 'read'):
				file_hash = calculate_file_hash(profile_pic)
				existing_file = FileModel.objects.filter(hash=file_hash).first()

				if existing_file:
					user_profile.profile_pic = existing_file.file_id
					existing_file.reference_count += 1
					existing_file.save()
				else:
					id = upload_file_to_appwrite(profile_pic.read(), filename=profile_pic.name)
					user_profile.profile_pic = id	
					FileModel.objects.create(hash=file_hash, file_id=id, reference_count=1)

				if self.instance.profile_pic:
					cleanup_unnecessary_file(self.instance.profile_pic)

		if cover_pic:=self.cleaned_data['cover_pic']:
			file_hash = calculate_file_hash(cover_pic)
			existing_file = FileModel.objects.filter(hash=file_hash).first()

			if existing_file:
				user_profile.cover_pic = existing_file.file_id
				existing_file.reference_count += 1
				existing_file.save()
			else:
				id = upload_file_to_appwrite(cover_pic.read(), filename=cover_pic.name)
				user_profile.cover_pic = id	
				FileModel.objects.create(hash=file_hash, file_id=id, reference_count=1)

			if self.instance.cover_pic:
				cleanup_unnecessary_file(self.instance.cover_pic)

		if commit:
			user_profile.save()
		return user_profile
