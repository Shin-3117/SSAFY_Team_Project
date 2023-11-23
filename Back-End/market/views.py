from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef
import requests
from datetime import datetime, date, timedelta
from .serializers import OilSerializer, GoldSerializer, KospiSeriesSerializer, KosdaqSeriesSerializer, KrxSeriesSerializer, ThemeIndexSerializer
from .models import Oil, Gold, KospiSeries, KosdaqSeries, KrxSeries, ThemeIndex
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.cache import cache_page

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# 투자 추천 알고리즘(최신 데이터 날짜 기준으로 과거 n개의 데이터를 바탕으로 상승 / 하락세 판별 => 기울기로 응답)
def calculate_investment_indicator(df, price_column):
    if df.empty:
        return None

    # 선형 회귀 모델 생성
    model = LinearRegression()

    # 날짜를 숫자 형태로 변환
    df['date_ordinal'] = pd.to_datetime(df['basDt']).apply(lambda x: x.toordinal())

    # 선형 회귀 모델 훈련
    model.fit(df[['date_ordinal']], df[price_column])

    # 선형 회귀 모델의 기울기 반환
    trend_slope = model.coef_[0]

    return trend_slope

@api_view(['GET'])
@cache_page(60 * 15)
def recommend_data(request, cnt):
    gold_instances = Gold.objects.order_by('-basDt')
    gold_serializer = GoldSerializer(gold_instances, many=True)
    gold_data = gold_serializer.data
    oil_instances = Oil.objects.order_by('-basDt')
    oil_serializer = OilSerializer(oil_instances, many=True)
    oil_data = oil_serializer.data
    kospi_instances = KospiSeries.objects.order_by('-basDt')
    kospi_serializer = KospiSeriesSerializer(kospi_instances, many=True)
    kospi_data = kospi_serializer.data
    kosdaq_instances = KosdaqSeries.objects.order_by('-basDt')
    kosdaq_serializer = KosdaqSeriesSerializer(kosdaq_instances, many=True)
    kosdaq_data = kosdaq_serializer.data
    krx_instances = KrxSeries.objects.order_by('-basDt')
    krx_serializer = KrxSeriesSerializer(krx_instances, many=True)
    krx_data = krx_serializer.data
    theme_instances = ThemeIndex.objects.order_by('-basDt')
    theme_serializer = ThemeIndexSerializer(theme_instances, many=True)
    theme_data = theme_serializer.data

    # 데이터프레임으로 변환
    gold_df = pd.DataFrame(gold_data)
    oil_df = pd.DataFrame(oil_data)
    kospi_df = pd.DataFrame(kospi_data)
    kosdaq_df = pd.DataFrame(kosdaq_data)
    krx_df = pd.DataFrame(krx_data)
    theme_df = pd.DataFrame(theme_data)

    # 날짜 형식으로 변환
    gold_df['basDt'] = pd.to_datetime(gold_df['basDt'])
    oil_df['basDt'] = pd.to_datetime(oil_df['basDt'])
    kospi_df['basDt'] = pd.to_datetime(kospi_df['basDt'])
    kosdaq_df['basDt'] = pd.to_datetime(kosdaq_df['basDt'])
    krx_df['basDt'] = pd.to_datetime(krx_df['basDt'])
    theme_df['basDt'] = pd.to_datetime(theme_df['basDt'])

    # 숫자 타입 변환
    oil_df['wtAvgPrcDisc'] = pd.to_numeric(oil_df['wtAvgPrcDisc'])
    kospi_df['clpr'] = pd.to_numeric(kospi_df['clpr'])
    kosdaq_df['clpr'] = pd.to_numeric(kosdaq_df['clpr'])
    krx_df['clpr'] = pd.to_numeric(krx_df['clpr'])
    theme_df['clpr'] = pd.to_numeric(theme_df['clpr'])

    # 최신 날짜부터 n일 간의 데이터 선택
    gold_recent = gold_df.head(cnt)
    oil_recent = oil_df.head(cnt*3)
    kospi_recent = kospi_df.head(cnt*46)
    kosdaq_recent = kosdaq_df.head(cnt*51)
    krx_recent = krx_df.head(cnt*28)
    theme_recent = theme_df.head(cnt*33)


    # 선택된 데이터를 오래된 날짜부터 최신 날짜 순으로 재정렬
    gold_recent.sort_values(by='basDt', inplace=True)
    oil_recent.sort_values(by='basDt', inplace=True)
    kospi_recent.sort_values(by='basDt', inplace=True)
    kosdaq_recent.sort_values(by='basDt', inplace=True)
    krx_recent.sort_values(by='basDt', inplace=True)
    theme_recent.sort_values(by='basDt', inplace=True)

    # 투자 지표 계산
    gold_indicator = calculate_investment_indicator(gold_recent, 'clpr')

    oil_indicators = {}
    for category in oil_recent['oilCtg'].unique():
        category_data = oil_recent[oil_recent['oilCtg'] == category]
        oil_indicators[category] = calculate_investment_indicator(category_data, 'wtAvgPrcDisc')
    
    kospi_indicators = {}
    for category in kospi_recent['idxNm'].unique():
        category_data = kospi_recent[kospi_recent['idxNm'] == category]
        kospi_indicators[category] = calculate_investment_indicator(category_data, 'clpr')
    
    kosdaq_indicators = {}
    for category in kosdaq_recent['idxNm'].unique():
        category_data = kosdaq_recent[kosdaq_recent['idxNm'] == category]
        kosdaq_indicators[category] = calculate_investment_indicator(category_data, 'clpr')
    
    krx_indicators = {}
    for category in krx_recent['idxNm'].unique():
        category_data = krx_recent[krx_recent['idxNm'] == category]
        krx_indicators[category] = calculate_investment_indicator(category_data, 'clpr')
    
    theme_indicators = {}
    for category in theme_recent['idxNm'].unique():
        category_data = theme_recent[theme_recent['idxNm'] == category]
        theme_indicators[category] = calculate_investment_indicator(category_data, 'clpr')

    # 각 카테고리별 추세 지표를 기울기에 따라 내림차순으로 정렬
    sorted_oil_indicators = sorted(oil_indicators.items(), key=lambda x: x[1], reverse=True)
    sorted_kospi_indicators = sorted(kospi_indicators.items(), key=lambda x: x[1], reverse=True)
    sorted_kosdaq_indicators = sorted(kosdaq_indicators.items(), key=lambda x: x[1], reverse=True)
    sorted_krx_indicators = sorted(krx_indicators.items(), key=lambda x: x[1], reverse=True)
    sorted_theme_indicators = sorted(theme_indicators.items(), key=lambda x: x[1], reverse=True)

    # 결과 정렬 및 JSON 형식으로 포맷팅
    response_data = {
        "금": [{"Name": "금", "Indicator": round(gold_indicator, 2)}],
        "석유": [{"Name": name, "Indicator": round(value, 2)} for name, value in sorted_oil_indicators],
        "KOSPI": [{"Name": name, "Indicator": round(value, 2)} for name, value in sorted_kospi_indicators],
        "KOSDAQ": [{"Name": name, "Indicator": round(value, 2)} for name, value in sorted_kosdaq_indicators],
        "KRX": [{"Name": name, "Indicator": round(value, 2)} for name, value in sorted_krx_indicators],
        "테마": [{"Name": name, "Indicator": round(value, 2)} for name, value in sorted_theme_indicators]
    }

    return JsonResponse(response_data)


# 일반 상품(석유, 금)
# Url
BASE_URL = "http://apis.data.go.kr/1160100/service/GetGeneralProductInfoService"
OIL_URL = "/getOilPriceInfo"
GOLD_URL = "/getGoldPriceInfo"
# 주가지수시세
STOCK_URL = 'http://apis.data.go.kr/1160100/service/GetMarketIndexInfoService/getStockMarketIndex'
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
            oil_instances = Oil.objects.order_by('-basDt')
            oil_serializer = OilSerializer(oil_instances, many=True)
            return Response(oil_serializer.data)
        
        elif code == 'gold':
            gold_instances = Gold.objects.order_by('-basDt')
            gold_serializer = GoldSerializer(gold_instances, many=True)
            return Response(gold_serializer.data)
        
        elif code == 'kospi':
            kospi_instances = KospiSeries.objects.order_by('-basDt')
            kospi_serializer = KospiSeriesSerializer(kospi_instances, many=True)
            return Response(kospi_serializer.data)
        
        elif code == 'kosdaq':
            kosdaq_instances = KosdaqSeries.objects.order_by('-basDt')
            kosdaq_serializer = KosdaqSeriesSerializer(kosdaq_instances, many=True)
            return Response(kosdaq_serializer.data)
        
        elif code == 'krx':
            krx_instances = KrxSeries.objects.order_by('-basDt')
            krx_serializer = KrxSeriesSerializer(krx_instances, many=True)
            return Response(krx_serializer.data)
        
        elif code == 'theme':
            theme_instances = ThemeIndex.objects.order_by('-basDt')
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