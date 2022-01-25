# tweet/models.py
from django.db import models
from user.models import UserModel #user앱에 있는 usermodel이라는 모델을 가져와 쓰겠다.
from taggit.managers import TaggableManager

# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE) #다른DB에서 모델을 가져와 넣겠다.
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True) #빈칸이어도 실행
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TweetComment(models.Model):
    class Meta:
        db_table = "comment"

    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)