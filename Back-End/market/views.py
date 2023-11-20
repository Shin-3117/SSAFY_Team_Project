from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import requests
from datetime import datetime
from .serializers import OilSerializer, GoldSerializer
from .models import Oil, Gold
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.cache import cache_page


# 일반 상품(석유, 금)
# Url
BASE_URL = "https://apis.data.go.kr/1160100/service/GetGeneralProductInfoService"
OIL_URL = "/getOilPriceInfo"
GOLD_URL = "/getGoldPriceInfo"
# api_key
API_KEY3 = settings.API_KEY3

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_test(request, code):
    if code == 'oil':
        url = BASE_URL + OIL_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'numOfRows': 2875,
        }
    elif code == 'gold':
        url = BASE_URL + GOLD_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'numOfRows': 959,
            'isinCd': 'KRD040200002'
        }
    response = requests.get(url, params=params).json()
    return Response(response)


# DB에 저장(석유)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def save_oil(request):
    try:
        url = BASE_URL + OIL_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'numOfRows': 2875,
        }
        response = requests.get(url, params=params).json()
        items = response.get('response').get('body').get('items').get('item')
        for item in items:
            item['basDt'] = datetime.strptime(item['basDt'], '%Y%m%d').date()
            serializer = OilSerializer(data=item)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return JsonResponse({'message': 'okay'})

    # API 요청 실패 시 처리
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    # 기타 예외 처리
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# DB에 저장(금)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def save_gold(request):
    try:
        url = BASE_URL + GOLD_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'numOfRows': 959,
            'isinCd': 'KRD040200002'
        }
        response = requests.get(url, params=params).json()
        items = response.get('response').get('body').get('items').get('item')
        for item in items:
            item['basDt'] = datetime.strptime(item['basDt'], '%Y%m%d').date()
            serializer = GoldSerializer(data=item)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return JsonResponse({'message': 'okay'})

    # API 요청 실패 시 처리
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    # 기타 예외 처리
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@cache_page(60 * 15)
def send_data(request, code):
    try:
        if code == 'oil':
            oil_instances = Oil.objects.all()
            oil_serializer = OilSerializer(oil_instances, many=True)
            return Response(oil_serializer.data)
        
        elif code == 'gold':
            gold_instances = Gold.objects.all()
            gold_serializer = GoldSerializer(gold_instances, many=True)
            return Response(gold_serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)