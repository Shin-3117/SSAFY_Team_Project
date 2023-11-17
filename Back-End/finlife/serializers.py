from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, DepositSubscription, SavingSubscription


class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)


class DepositSerializer(serializers.ModelSerializer):
    fin_prdt_cd = DepositProductsSerializer(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = DepositOptions
        fields = '__all__'
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if DepositSubscription.objects.filter(
                user=request.user,
                deposit_option=obj
            ).exists():
                print("CHECK")
                return True
            else:
                return False


class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)


class SavingSerializer(serializers.ModelSerializer):
    fin_prdt_cd = SavingProductsSerializer(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = SavingOptions
        fields = '__all__'
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if SavingSubscription.objects.filter(
                user=request.user,
                saving_option=obj
            ).exists():
                print("CHECK")
                return True
            else:
                return False


class DepositSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositSubscription
        fields = '__all__'
        read_only_fields = ('user',)


class SavingSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingSubscription
        fields = '__all__'
        read_only_fields = ('user',)



