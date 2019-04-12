from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta: # 일관성이 있다.
        model = Post
        fields = ['content',]