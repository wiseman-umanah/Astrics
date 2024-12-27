from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm


class LoginForm(forms.Form):
	username = forms.CharField(min_length=2, required=True,
							widget=forms.TextInput(attrs={
								'placeholder': 'Enter your Username or Email'
							}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Enter your password'}), required=True)
		


class RegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Password'
	}), max_length=16, min_length=8, required=True)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Confirm password'
	}), required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email', 'last_name')
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
			'placeholder': 'Username',
		})
		self.fields['first_name'].widget.attrs.update({
			'placeholder': 'First name',
		})
		self.fields['last_name'].widget.attrs.update({
			'placeholder': 'Last name (optional)',
		})
		self.fields['email'].widget.attrs.update({
			'placeholder': 'Email',
		})

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("Passwords don't match.")
		return cd['password2']

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("A user with this email already exist")
		return email

class CustomPasswordForm(SetPasswordForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
		self.fields['new_password1'].widget.attrs.update({
			'placeholder': 'Enter your new password',
			'minlength': '8',
			'maxlength': '16',
		})
		self.fields['new_password2'].widget.attrs.update({
			'placeholder': 'Confirm your new password',
			'minlength': '8',
			'maxlength': '16',
		})
