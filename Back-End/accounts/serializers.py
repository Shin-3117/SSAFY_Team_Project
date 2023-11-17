from dj_rest_auth.registration.serializers import RegisterSerializer
# from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from articles.serializers import ArticleListSerializer, ProfileCommentSerializer
from django.contrib.auth import get_user_model

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


class UserDetailSerializer(serializers.ModelSerializer):
    written_articles = ArticleListSerializer(source='article_set', many=True, read_only=True)
    written_comments = ProfileCommentSerializer(source='comment_set', many=True, read_only=True)
    liked_articles = ArticleListSerializer(source='like_articles', many=True, read_only=True)
    followings_list = UserSerializer(source='followings', many=True, read_only=True)
    followers_list = UserSerializer(source='followers', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'gender', 'birthday', 'money', 'written_articles', 'written_comments', 'liked_articles', 'followings_list', 'followers_list',)



# class CustomLoginSerializer(LoginSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'password')
#         extra_kwargs = {'password': {'write_only': True}}