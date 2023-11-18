from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.api_test),
    path('save_deposit/', views.save_deposit),
    path('save_saving/', views.save_saving),
    path('deposit/<int:term>/<str:sort_field>/', views.deposit_products), # 예금 상품 조회
    path('saving/<int:term>/<str:sort_field>/', views.saving_products), # 적금 상품 조회
    path('subscribe_deposit/', views.subscribe_deposit), # 예금 상품 구독하기(request에 page번호 넘겨줘야 캐시 삭제하여 상태 갱신 가능)
    path('subscribe_saving/', views.subscribe_saving), # 적금 상품 구독하기(request에 page번호 넘겨줘야 캐시 삭제하여 상태 갱신 가능)
    # path('save_deposit2/', views.save_deposit2),
]
