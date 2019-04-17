from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.conf import settings

from .models import Profile
class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email',]

class UserEditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['email',]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )