from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from articles.serializers import ArticleListSerializer, ProfileCommentSerializer
from finlife.serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer
from finlife.models import DepositSubscription, SavingSubscription
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model() 


class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, default=0)
    birthday = serializers.DateField()
    money = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'birthday', 'money',)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['gender'] = self.validated_data.get('gender', 0)
        data['birthday'] = self.validated_data['birthday']
        data['money'] = self.validated_data.get('money', 0)
        return data

    def save(self, request):
        user = super().save(request)
        user.gender = self.validated_data.get('gender', 0)
        user.birthday = self.validated_data['birthday']
        user.money = self.validated_data.get('money', 0)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class DepositSubscriptionSerializer(serializers.ModelSerializer):
    deposit_product_detail = DepositProductsSerializer(source='deposit_product', read_only=True)
    deposit_option_detail = DepositOptionsSerializer(source='deposit_option', read_only=True)

    class Meta:
        model = DepositSubscription
        fields = ('deposit_product_detail', 'deposit_option_detail', 'subscribe_date',)


class SavingSubscriptionSerializer(serializers.ModelSerializer):
    saving_product_detail = SavingProductsSerializer(source='saving_product', read_only=True)
    saving_option_detail = SavingOptionsSerializer(source='saving_option', read_only=True)

    class Meta:
        model = SavingSubscription
        fields = ('saving_product_detail', 'saving_option_detail', 'subscribe_date',)


class UserDetailSerializer(serializers.ModelSerializer):
    written_articles = ArticleListSerializer(source='article_set', many=True, read_only=True)
    written_comments = ProfileCommentSerializer(source='comment_set', many=True, read_only=True)
    liked_articles = ArticleListSerializer(source='like_articles', many=True, read_only=True)
    followings_list = UserSerializer(source='followings', many=True, read_only=True)
    followers_list = UserSerializer(source='followers', many=True, read_only=True)
    deposit_subscriptions = DepositSubscriptionSerializer(source='depositsubscription_set', many=True, read_only=True)
    saving_subscriptions = SavingSubscriptionSerializer(source='savingsubscription_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'gender', 'birthday', 'money', 'written_articles', 'written_comments', 'liked_articles', 'followings_list', 'followers_list', 'deposit_subscriptions', 'saving_subscriptions',)


class DeleteUserSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'gender', 'birthday', 'money',)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value