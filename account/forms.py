from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(min_length=2, required=True)
	password = forms.CharField(widget=forms.PasswordInput, min_length=8,
							max_length=16, required=True)
