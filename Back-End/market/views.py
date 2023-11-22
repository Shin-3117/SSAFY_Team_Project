from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef, Max
import requests
from datetime import datetime, date, timedelta
from .serializers import OilSerializer, GoldSerializer, KospiSeriesSerializer, KosdaqSeriesSerializer, KrxSeriesSerializer, ThemeIndexSerializer
from .models import Oil, Gold, KospiSeries, KosdaqSeries, KrxSeries, ThemeIndex
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.cache import cache_page


# 일반 상품(석유, 금)
# Url
BASE_URL = "https://apis.data.go.kr/1160100/service/GetGeneralProductInfoService"
OIL_URL = "/getOilPriceInfo"
GOLD_URL = "/getGoldPriceInfo"
# 주가지수시세
STOCK_URL = 'https://apis.data.go.kr/1160100/service/GetMarketIndexInfoService/getStockMarketIndex'
# api_key
API_KEY3 = settings.API_KEY3

# Create your views here.
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def api_test(request, code):
    if code == 'oil':
        url = BASE_URL + OIL_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'beginBasDt': str(date.today() - timedelta(days=2)).replace("-", "")
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
# @permission_classes([IsAdminUser])
def save_oil(request):
    try:
        url = BASE_URL + OIL_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'beginBasDt': str(date.today() - timedelta(days=1)).replace("-", ""),
        }
        response = requests.get(url, params=params).json()
        items = response.get('response').get('body').get('items').get('item')
        for item in items:
            if item['wtAvgPrcDisc'] == '0':
                continue
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
# @permission_classes([IsAdminUser])
def save_gold(request):
    try:
        url = BASE_URL + GOLD_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'isinCd': 'KRD040200002',
            'beginBasDt': str(date.today() - timedelta(days=1)).replace("-", ""),
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


# DB에 저장(주가지수시세)
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def save_stock(request):
    try:
        url = STOCK_URL
        params = {
            'serviceKey': API_KEY3,
            'resultType': 'json',
            'numOfRows': 1000,
            'beginBasDt': str(date.today() - timedelta(days=1)).replace("-", ""),
        }
        response = requests.get(url, params=params).json()
        items = response.get('response').get('body').get('items').get('item')
        for item in items:
            item['basDt'] = datetime.strptime(item['basDt'], '%Y%m%d').date()
            if item['idxCsf'] == "KOSPI시리즈":
                serializer = KospiSeriesSerializer(data=item)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            elif item['idxCsf'] == "KOSDAQ시리즈":
                serializer = KosdaqSeriesSerializer(data=item)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            elif item['idxCsf'] == "KRX시리즈":
                serializer = KrxSeriesSerializer(data=item)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            elif item['idxCsf'] == "테마지수":
                serializer = ThemeIndexSerializer(data=item)
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
        
        elif code == 'kospi':
            kospi_instances = KospiSeries.objects.all()
            kospi_serializer = KospiSeriesSerializer(kospi_instances, many=True)
            return Response(kospi_serializer.data)
        
        elif code == 'kosdaq':
            kosdaq_instances = KosdaqSeries.objects.all()
            kosdaq_serializer = KosdaqSeriesSerializer(kosdaq_instances, many=True)
            return Response(kosdaq_serializer.data)
        
        elif code == 'krx':
            krx_instances = KrxSeries.objects.all()
            krx_serializer = KrxSeriesSerializer(krx_instances, many=True)
            return Response(krx_serializer.data)
        
        elif code == 'theme':
            theme_instances = ThemeIndex.objects.all()
            theme_serializer = ThemeIndexSerializer(theme_instances, many=True)
            return Response(theme_serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@cache_page(60 * 15)
def send_main(request, code):
    try:
        if code == 'oil':
            # 각 유종별로 최신 날짜 기준의 7개 데이터를 가져오기 위한 쿼리셋
            recent_oils_per_category = Oil.objects.filter(
                basDt__in=Subquery(
                    Oil.objects.filter(
                        oilCtg=OuterRef('oilCtg')
                    ).order_by('-basDt').values('basDt')[:7]
                )
            ).order_by('oilCtg', '-basDt')

            oil_serializer = OilSerializer(recent_oils_per_category, many=True)
            return Response(oil_serializer.data)
        
        elif code == 'gold':
            gold_instances = Gold.objects.order_by('-basDt')[:7]
            gold_serializer = GoldSerializer(gold_instances, many=True)
            return Response(gold_serializer.data)
        
        elif code == 'kospi':
            kospi_instances = KospiSeries.objects.filter(idxNm='코스피').order_by('-basDt')[:7]
            kospi_serializer = KospiSeriesSerializer(kospi_instances, many=True)
            return Response(kospi_serializer.data)
        
        elif code == 'kosdaq':
            kosdaq_instances = KosdaqSeries.objects.filter(idxNm='코스닥').order_by('-basDt')[:7]
            kosdaq_serializer = KosdaqSeriesSerializer(kosdaq_instances, many=True)
            return Response(kosdaq_serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)