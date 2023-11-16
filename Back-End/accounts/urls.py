from django.urls import path
from .views import profile_view, follow

urlpatterns = [
    path('profile/<str:username>/', profile_view, name='profile'),
    path('<int:user_pk>/follow/', follow, name='follow'),
]