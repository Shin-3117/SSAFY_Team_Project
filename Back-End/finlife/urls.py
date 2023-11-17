from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.api_test),
    path('save_deposit/', views.save_deposit),
    path('save_saving/', views.save_saving),
    path('deposit/<int:term>/<str:sort_field>/', views.deposit_products),
    path('saving/<int:term>/<str:sort_field>/', views.saving_products),
    path('subscribe_deposit/', views.subscribe_deposit),
    path('subscribe_saving/', views.subscribe_saving),
    # path('save_deposit2/', views.save_deposit2),
]
