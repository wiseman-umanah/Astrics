from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm


class LoginForm(forms.Form):
	username = forms.CharField(min_length=2, required=True,
							widget=forms.TextInput(attrs={
								'placeholder': 'Enter your Username or Email',
								'aria-label': 'Username',
								'aria-invalid': 'true',
								'aria-required': 'true'
							}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Enter your password',
		'aria-label': 'Password',
		'aria-invalid': 'true',
		'aria-required': 'true'}), required=True)
		


class RegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Password',
		'aria-label': 'Password',
		'aria-invalid': 'true',
		'aria-required': 'true'
	}), max_length=16, min_length=8, required=True)

	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Confirm password',
		'aria-label': 'Confirm Password',
		'aria-invalid': 'true',
		'aria-required': 'true'
	}), required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email', 'last_name')
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
			'placeholder': 'Username',
			'aria-label': 'Username',
			'aria-invalid': 'true',
			'aria-required': 'true'
		})
		self.fields['first_name'].widget.attrs.update({
			'placeholder': 'First name',
			'aria-label': 'First Name',
			'aria-invalid': 'true',
			'aria-required': 'true'
		})
		self.fields['last_name'].widget.attrs.update({
			'placeholder': 'Last name (optional)',
			'aria-label': 'Last Name Optional'
		})
		self.fields['email'].widget.attrs.update({
			'placeholder': 'Email',
			'aria-label': 'Email Address',
			'aria-invalid': 'true',
			'aria-required': 'true'
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
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("A user with this username already exist")
		return username


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
