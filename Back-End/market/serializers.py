from rest_framework import serializers
from .models import Oil, Gold, KospiSeries, KosdaqSeries, KrxSeries, ThemeIndex


class OilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = '__all__'


class GoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gold
        fields = '__all__'


class KospiSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiSeries
        fields = '__all__'


class KosdaqSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqSeries
        fields = '__all__'


class KrxSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KrxSeries
        fields = '__all__'


class ThemeIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeIndex
        fields = '__all__'