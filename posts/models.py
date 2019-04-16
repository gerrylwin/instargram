from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user.post_set.all() - 게시글 ? 좋아요 한 글 ? 이 중복을 방지 하기 위해
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts") # 가시성이 좋게 like를 붙임
    # image = models.ImageField()                               # relate_name을 써서 중복방지
    
    @property # property 를 쓰면 함수를 호출할 때 like_count() 가 아닌 like_count 로 값만을 호출할때 쓰인다. ( ex : 좋아요)
    def like_count(self):
        return self.like_users.count()
    
    def __str__(self):
        return f'POST : {self.pk}'
    
    def get_absolute_url(self):
        return reverse('posts:detail', args=[self.pk])
        
class Image(models.Model):
    file = models.ImageField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)