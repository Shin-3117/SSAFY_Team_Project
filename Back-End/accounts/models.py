from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # 유저 간 팔로우 - 팔로잉 필드
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # 성별 선택 필드
    GENDER_CHOICES = [
        (0,'male'),
        (1, 'female'),
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
