from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email',]

class UserEditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email',]