from django.db import models
from django.contrib.auth.models import AbstractUser
from finlife.models import DepositProducts, SavingProducts, DepositSubscription, SavingSubscription


# Create your models here.
class User(AbstractUser):
    # 유저 간 팔로우 - 팔로잉 필드
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    # 성별 선택 필드
    GENDER_CHOICES = [
        (0,'male'),
        (1, 'female'),
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    # 생년월일 필드
    birthday = models.DateField()
    # 보유자산 필드
    money = models.IntegerField(default=0)
    # 예금 상품 가입 정보
    deposit_subscriptions = models.ManyToManyField(
        DepositProducts,
        through=DepositSubscription,
        related_name='subscribed_users'
    )
    # 적금 상품 가입 정보
    saving_subscriptions = models.ManyToManyField(
        SavingProducts,
        through=SavingSubscription,
        related_name='subscribed_users'
    )