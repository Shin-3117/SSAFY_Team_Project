from rest_framework import serializers
from .models import Oil, Gold


class OilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = '__all__'


class GoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gold
        fields = '__all__'