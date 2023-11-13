from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import requests
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions


# 기본 url
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# 예금 url
DEPOSIT_URL = 'depositProductsSearch.json'
# 적금 url
SAVING_URL = 'savingProductsSearch.json'
# api key
API_KEY = settings.API_KEY


# Create your views here.
# API 응답 테스트
@api_view(['GET'])
def api_test(request):
    url = BASE_URL + SAVING_URL
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(url, params=params).json()
    return Response(response)


# 예금 API 요청 -> DB 저장
@api_view(['GET'])
def save_deposit(request):
    try:
        url = BASE_URL + DEPOSIT_URL
        params = {
            'auth': API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': 1
        }

        response = requests.get(url, params=params).json()
        baseList = response.get('result').get('baseList')
        optionList = response.get('result').get('optionList')

        # 상품 데이터 저장
        for product_data in baseList:
            product_serializer = DepositProductsSerializer(data=product_data)
            if product_serializer.is_valid(raise_exception=True):
                if DepositProducts.objects.filter(fin_prdt_cd=product_data['fin_prdt_cd']).exists():
                    continue
                product_serializer.save()
        
        # 옵션 데이터 저장
        
    except requests.RequestException as e:
        # API 요청 실패 시 처리
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        # 기타 예외 처리
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


# 적금 API 요청 -> DB 저장
@api_view(['GET'])
def save_saving(request):
    pass


@api_view(['GET'])
def deposit_products(request):
    pass


@api_view(['GET'])
def deposit_options(request):
    pass


@api_view(['GET'])
def saving_products(request):
    pass


@api_view(['GET'])
def saving_options(request):
    pass
