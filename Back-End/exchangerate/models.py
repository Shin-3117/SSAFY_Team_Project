from django.db import models

# Create your models here.
class ExchangeRates(models.Model):
    # 통화코드
    cur_unit = models.CharField(max_length=10)
    # 국가/통화명(공백으로 구분)
    cur_nm = models.CharField(max_length=50)
    # 송금 받을때 가격
    ttb = models.DecimalField(max_digits=12, decimal_places=4)
    # 송금 보낼때 가격
    tts = models.DecimalField(max_digits=12, decimal_places=4)
    # 매매기준율
    deal_bas_r = models.DecimalField(max_digits=12, decimal_places=4)
    # 한화 1000원당 해당국가 통화가격
    krw_to_cur = models.DecimalField(max_digits=10, decimal_places=2)
    # 요청날짜
    req_dt = models.DateField()
