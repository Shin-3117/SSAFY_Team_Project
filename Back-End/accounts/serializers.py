from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, default=0)
    birthday = serializers.DateField()
    money = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'birthday', 'money')

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