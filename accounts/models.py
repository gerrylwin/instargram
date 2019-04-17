from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings")

class Profile(models.Model):                                                        # CASCADE 는
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # user가 삭제가 될때
    nickname = models.CharField(max_length=30)                                      # Profile도 같이 삭제
    introduction = models.TextField()
    image = ProcessedImageField(
                    processors=[ResizeToFill(300, 300)],
                    format="JPEG",
                    options = {'quality': 80},
        )