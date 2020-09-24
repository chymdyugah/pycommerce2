from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control login-input', 'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control login-input', 'placeholder': 'Password'}))


class RegistrationForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control login-input', 'placeholder': 'First Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control login-input', 'placeholder': 'Last Name'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control login-input', 'placeholder': 'Email'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control login-input', 'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control login-input', 'placeholder': 'Password'}))

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password']
