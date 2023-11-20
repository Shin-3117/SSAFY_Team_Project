from django.urls import path
from .views import profile_view, follow, user_operations

urlpatterns = [
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<int:user_pk>/', follow, name='follow'),
    path('user/', user_operations, name='user_operations'),
]