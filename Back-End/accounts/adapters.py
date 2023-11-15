from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        # 기본적인 사용자 저장 로직
        user = super().save_user(request, user, form, commit=False)
        # 커스텀 필드 데이터를 user 모델 인스턴스에 추가
        user.gender = form.cleaned_data.get('gender')
        user.birthday = form.cleaned_data.get('birthday')
        user.money = form.cleaned_data.get('money')
        # 변경 사항을 데이터베이스에 저장
        if commit:
            user.save()
        return user