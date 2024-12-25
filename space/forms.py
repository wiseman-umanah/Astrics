from django.contrib.auth.models import User
from django import forms
from account.models import UserProfile
from utils.utils import upload_file_to_appwrite



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
        fields = ('user', 'profile_pic', 'cover_pic')

    def save(self, commit=True):
        user_profile = super().save(commit=False)

        if self.cleaned_data['profile_pic']:
            file = self.cleaned_data['profile_pic']
            filename = file.name
            id = upload_file_to_appwrite(file, filename)
            user_profile.profile_pic = id

        if self.cleaned_data['cover_pic']:
            file = self.cleaned_data['cover_pic']
            filename = file.name
            id = upload_file_to_appwrite(file, filename)
            user_profile.cover_pic = id

        if commit:
            user_profile.save()
        return user_profile
