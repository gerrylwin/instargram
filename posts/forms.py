from django.forms import ModelForm
from .models import Post, Image, Comment
from django import forms

class PostForm(ModelForm):
    class Meta: # 일관성이 있다.
        model = Post
        fields = ['content']
        
class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['post']
        widgets = {
            'file': forms.FileInput(attrs={'multiple': True}),
        }

class CommentForm(ModelForm):
    class Meta: # 일관성이 있다.
        model = Comment
        fields = ['comment']

        