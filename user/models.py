# user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser # 장고에서 사용하는 기본적인 유저모델(AbstractUser)을 사용하겠다.
from django.conf import settings
#from mySpartaSns import settings 이렇게 부를수도 있지만 장고가 관리하는 세팅을 불러오는게 좋다.

# Create your models here.
class UserModel(AbstractUser): # 장고기본모델에서 추가해서 사용 UserModel에서 사용/class상속 사용/settings.py에서 설정
   class Meta: # db테이블의 정보를 넣어준다
        db_table = "my_user"

   bio = models.CharField(max_length=256, default='') # 상태정보추가
   follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee') #우리유저모델을 불러옴

   # username = models.CharField(max_length=20, null=False) # CharField>모델필드의 종류
   # password = models.CharField(max_length=256, null=False)
   # created_at = models.DateTimeField(auto_now_add=True) # 생성일
   # updated_at = models.DateTimeField(auto_now=True) # 수정일

