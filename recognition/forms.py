from django.contrib.auth.models import User
from django import forms
from .models import FaceSignature, UserProfile

class UserRegForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username','email','password')

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email',)

class UserLoginForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	password.widget.attrs.update({'class': 'form-control'})
	class Meta:
		model = User
		fields = ('username','password')

class UserFaceRegForm(forms.ModelForm):
	class Meta:
		model = FaceSignature
		fields={}

class UserProfileForm(forms.ModelForm):
	"""docstring for UserProfileForm"""
	class Meta:
		model = UserProfile
		fields = ('firstname','lastname','website','bio','phone','photo','city','country','organization')
		