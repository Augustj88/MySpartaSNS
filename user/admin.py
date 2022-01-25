
from django.contrib import admin #장고에서 admin 툴사용
from .models import UserModel #우리가 생성한 모델을 가져온다. (models의 usermodel을 가져온다)

# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다