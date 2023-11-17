from django.urls import path
from .views import profile_view, follow, delete_user

urlpatterns = [
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<int:user_pk>/', follow, name='follow'),
    path('delete_user/', delete_user, name='delete_user'),
]