from rest_framework import serializers
from .models import ExchangeRates

class ExchangeRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = '__all__'
        read_only_fields = ('req_dt',)