from django.db import models
from django.conf import settings


# Create your models here.
# 예금 상품 목록
class DepositProducts(models.Model):
    # 금융 상품 코드
    fin_prdt_cd = models.TextField(unique=True)
    # 금융 회사명
    kor_co_nm = models.TextField()
    # 금융 상품명
    fin_prdt_nm = models.TextField()
    # 금융 상품 설명
    etc_note = models.TextField()
    # 가입 제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_deny = models.IntegerField()
    # 가입 대상
    join_member = models.TextField()
    # 가입 방법
    join_way = models.TextField()
    # 우대 조건
    spcl_cnd = models.TextField()


# 예금 옵션 목록
class DepositOptions(models.Model):
    # 금융 상품 코드(왜래키)
    fin_prdt_cd = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='depositoptions')
    # 저축금리 유형
    intr_rate_type = models.TextField()
    # 저축금리 유형명
    intr_rate_type_nm = models.CharField(max_length=100)
    # 저축금리
    intr_rate = models.FloatField(default=-1, null=True, blank=True)
    # 최고우대금리
    intr_rate2 = models.FloatField()
    # 저축기간(단위: 개월)
    save_trm = models.IntegerField()


# 적금 상품 목록
class SavingProducts(models.Model):
    # 금융 상품 코드
    fin_prdt_cd = models.TextField(unique=True)
    # 금융 회사명
    kor_co_nm = models.TextField()
    # 금융 상품명
    fin_prdt_nm = models.TextField()
    # 금융 상품 설명
    etc_note = models.TextField()
    # 가입 제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_deny = models.IntegerField()
    # 가입 대상
    join_member = models.TextField()
    # 가입 방법
    join_way = models.TextField()
    # 우대 조건
    spcl_cnd = models.TextField()


# 적금 옵션 목록
class SavingOptions(models.Model):
    # 금융 상품 코드(왜래키)
    fin_prdt_cd = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='savingoptions')
    # 저축금리 유형
    intr_rate_type = models.TextField()
    # 저축금리 유형명
    intr_rate_type_nm = models.CharField(max_length=100)
    # 저축금리
    intr_rate = models.FloatField(default=-1, null=True, blank=True)
    # 최고우대금리
    intr_rate2 = models.FloatField()
    # 저축기간(단위: 개월)
    save_trm = models.IntegerField()
    # 적립 유형
    rsrv_type = models.TextField()
    # 적립 유형명
    rsrv_type_nm = models.CharField(max_length=100)


# 예금 상품 가입 중간 모델
class DepositSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deposit_product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    deposit_option = models.ForeignKey(DepositOptions, on_delete=models.CASCADE)
    subscribe_date = models.DateTimeField(auto_now_add=True)


# 적금 상품 가입 중간 모델
class SavingsSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saving_product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    saving_option = models.ForeignKey(SavingOptions, on_delete=models.CASCADE)
    subscribe_date = models.DateTimeField(auto_now_add=True)