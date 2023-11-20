from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_test),
    path('save_news/', views.save_news),
    path('data/<int:code>/', views.news_data),
]
