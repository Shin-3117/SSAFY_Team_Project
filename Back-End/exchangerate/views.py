from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import requests
from datetime import date
from .serializers import ExchangeRatesSerializer
from .models import ExchangeRates
from django.views.decorators.cache import cache_page
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Url
URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
# api_key
API_KEY = settings.API_KEY2

# Create your views here.
# API 응답 테스트
@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_test(request):
    url = URL
    params = {
        'authkey': API_KEY,
        'data': 'AP01',
        'searchdate': "20231115",
    }
    response = requests.get(url, params=params).json()
    return Response(response)


# 문자열에서 쉼표 제거하는 함수
def parse_float(value):
    try:
        return float(value.replace(',', ''))
    except ValueError:
        return None


# 환율 API 요청 -> DB 저장
@api_view(['GET'])
def save_rate(request):
    try:
        url = URL
        params = {
            'authkey': API_KEY,
            'data': 'AP01',
        }
        response = requests.get(url, params=params).json()

        today = date.today()

        # 환율 데이터 저장
        for rate_data in response:
            # 쉼표 제거 및 부동 소수점 변환
            deal_bas_r = parse_float(rate_data['deal_bas_r'])
            ttb = parse_float(rate_data['ttb'])
            tts = parse_float(rate_data['tts'])
            # 100 단위 기준 통화 처리(일본, 인도네시아)
            if "(100)" in rate_data['cur_unit']:
                rate_data['cur_unit'] = rate_data['cur_unit'].replace("(100)", "").strip()
                deal_bas_r = round(deal_bas_r / 100, 4)
                ttb = round(ttb / 100, 4)
                tts = round(tts / 100, 4)
            rate_data['deal_bas_r'] = deal_bas_r
            rate_data['ttb'] = ttb
            rate_data['tts'] = tts
            # 한화 1000원당 해당 통화 가격 계산
            if deal_bas_r > 0:
                krw_to_cur = round(1000 / deal_bas_r, 2)
                rate_data['krw_to_cur'] = krw_to_cur
            # 환율 정보가 없으면 DB에 저장하지 않음
            else:
                continue
            # 통화 코드 기준으로 DB에 존재 여부 확인
            rate_instance =  ExchangeRates.objects.filter(cur_unit=rate_data['cur_unit']).first()
            # 존재한다면
            if rate_instance:
                # 갱신 날짜 체크 -> 최신 데이터로 갱신
                if rate_instance.req_dt != today:
                    rate_serializer = ExchangeRatesSerializer(instance=rate_instance, data=rate_data)
                    if rate_serializer.is_valid(raise_exception=True):
                        rate_serializer.save()
            # 존재하지 않으면 추가
            else:
                rate_serializer = ExchangeRatesSerializer(data=rate_data)
                if rate_serializer.is_valid(raise_exception=True):
                    rate_serializer.save()
        return JsonResponse({'message': 'okay'})

    # API 요청 실패 시 처리
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    # 기타 예외 처리
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# DB에 저장된 환율 정보 응답
@api_view(['GET'])
# 캐싱 적용
@cache_page(60 * 15)
def rate_data(request, code):
    try:
        if code == 'ALL':
            rate_instances = ExchangeRates.objects.all()
            rates_serializer = ExchangeRatesSerializer(rate_instances, many=True)
            return Response(rates_serializer.data)
        else:
            rate_instance =  ExchangeRates.objects.filter(cur_unit=code).first()
            if rate_instance:
                rate_serializer = ExchangeRatesSerializer(rate_instance)
                return Response(rate_serializer.data)
            else:
                return Response({'error': 'Not found'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)