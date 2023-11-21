from django.db import models

# Create your models here.
class Oil(models.Model):
    # 일자
    basDt = models.DateField()
    # 유종
    oilCtg = models.TextField()
    # 협의거래 가중평균가격
    wtAvgPrcDisc = models.DecimalField(max_digits=10, decimal_places=2)


class Gold(models.Model):
    # 일자
    basDt = models.DateField()
    # 종목명
    itmsNm = models.TextField()
    # 종가
    clpr = models.IntegerField()


# 코스피 시리즈
class KospiSeries(models.Model):
    # 일자
    basDt = models.DateField()
    # 지수명
    idxNm = models.CharField(max_length=50)
    # 종가
    clpr = models.DecimalField(max_digits=10, decimal_places=2)


# 코스닥 시리즈
class KosdaqSeries(models.Model):
    # 일자
    basDt = models.DateField()
    # 지수명
    idxNm = models.CharField(max_length=50)
    # 종가
    clpr = models.DecimalField(max_digits=10, decimal_places=2)


# KRX 시리즈
class KrxSeries(models.Model):
    # 일자
    basDt = models.DateField()
    # 지수명
    idxNm = models.CharField(max_length=50)
    # 종가
    clpr = models.DecimalField(max_digits=10, decimal_places=2)


# 테마지수
class ThemeIndex(models.Model):
    # 일자
    basDt = models.DateField()
    # 지수명
    idxNm = models.CharField(max_length=50)
    # 종가
    clpr = models.DecimalField(max_digits=10, decimal_places=2)