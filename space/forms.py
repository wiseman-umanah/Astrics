from django.contrib.auth.models import User
from django import forms
from account.models import ( UserProfile, Post,
							Comment)
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

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
			raise forms.ValidationError("A user with this email already exist")
		return email
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
			raise forms.ValidationError("A user with this username already exist")
		return username


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
				raise forms.ValidationError("Profile Image must be less than 10MB.")
			file_hash = calculate_file_hash(profile_pic)

			existing_file = FileModel.objects.filter(hash=file_hash).first()
			if existing_file:
				existing_file.reference_count += 1
				cleanup_unnecessary_file(user_profile.profile_pic_id)
				existing_file.save()
				user_profile.profile_pic_id = existing_file.file_id
			else:
				cleanup_unnecessary_file(user_profile.profile_pic_id)
				profile_pic.seek(0)
				file_id = upload_file_to_appwrite(profile_pic.read(), filename=profile_pic.name)
				user_profile.profile_pic_id = file_id
				FileModel.objects.create(
										hash=file_hash,
							 			file_id=file_id,
							 			reference_count=1)
		
		if cover_pic:= self.cleaned_data.get('cover_pic'):
			if cover_pic.size > 10 * 1024 * 1024:
				raise forms.ValidationError("Cover Image must be less than 10MB.")
			file_hash = calculate_file_hash(cover_pic)

			existing_file = FileModel.objects.filter(hash=file_hash).first()
			if existing_file:
				existing_file.reference_count += 1
				cleanup_unnecessary_file(user_profile.cover_pic_id)
				existing_file.save()
				user_profile.cover_pic_id = existing_file.file_id
			else:
				cleanup_unnecessary_file(user_profile.cover_pic_id)
				cover_pic.seek(0)
				file_id = upload_file_to_appwrite(cover_pic.read(), filename=cover_pic.name)
				user_profile.cover_pic_id = file_id
				FileModel.objects.create(
										hash=file_hash,
							 			file_id=file_id,
							 			reference_count=1)
		

		user_profile.save()
		return user_profile


class AdminUserProfileForm(forms.ModelForm):
	profile_pic = forms.ImageField(required=False)
	cover_pic = forms.ImageField(required=False)

	class Meta:
		model = UserProfile
		fields = ("user", "profile_pic_id", "cover_pic_id", "follows")


class UserPostForm(forms.ModelForm):
	media_file = forms.FileField(
		widget=forms.FileInput(attrs={
			'id': 'id_media_file',
			'style': 'display: none;',
		}),required=False)

	class Meta:
		model = Post
		fields = ("title", "description",)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['description'].widget.attrs.update({
			'placeholder': 'Write your post here',
			'class': 'newpost_description',
			'rows': "1"
		})
		self.fields['title'].widget.attrs.update({
			'placeholder': 'Title (optional)',
		})
	
	def clean_media_file(self):
		media_file = self.cleaned_data.get("media_file")

		if media_file:
			print(media_file.size)
			if media_file.size > 10 * 1024 * 1024:
				raise forms.ValidationError("Media File must less than 10MB")
		
		return media_file
			
	def save(self, commit=True):
		instance = super().save(commit=False)
		media_file = self.cleaned_data.get("media_file")

		if media_file:
			if media_file.content_type.startswith('image'):
				instance.media_type = "image"
			elif media_file.content_type.startswith("video"):
				instance.media_type = "video"
			else:
				raise forms.ValidationError("Only Pictures and Videos of 10MB are Allowed")
			file_hash = calculate_file_hash(media_file)

			existing_file = FileModel.objects.filter(hash=file_hash).first()
			if existing_file:
				existing_file.reference_count += 1
				existing_file.save()
				instance.file_id = existing_file.file_id
			else:
				media_file.seek(0)
				file_id = upload_file_to_appwrite(media_file.read(), filename=media_file.name)
				instance.file_id = file_id
				FileModel.objects.create(
										hash=file_hash,
							 			file_id=file_id,
							 			reference_count=1)
		else:
			instance.media_type = 'text'
		
		if commit:
			instance.save()
		return instance


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)
