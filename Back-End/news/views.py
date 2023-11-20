from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import requests
from datetime import datetime
from .serializers import NewsSerializer
from .models import News


# Url
URL = 'https://openapi.naver.com/v1/search/news.json'
# api_key
API_ID = settings.API_ID
API_SECRET = settings.API_SECRET

# Create your views here.
@api_view(['GET'])
def api_test(request):
    url = URL
    headers = {
        'X-Naver-Client-Id': API_ID,
        'X-Naver-Client-Secret': API_SECRET
    }
    params = {
        'query': '경제뉴스',
        'sort': 'sim',
        'display': 100,
    }
    response = requests.get(url, headers=headers, params=params).json()
    return Response(response)


# DB에 저장
@api_view(['GET'])
def save_news(request):
    try:
        url = URL
        headers = {
            'X-Naver-Client-Id': API_ID,
            'X-Naver-Client-Secret': API_SECRET
        }
        params = {
            'query': '경제뉴스',
            'sort': 'date',
            'display': 100,
        }
        response = requests.get(url, headers=headers, params=params).json()
        News.objects.all().delete()
        items = response['items']
        for item in items:
            # 날짜와 시간 정보를 datetime 객체로 변환
            pubdate_dt = datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
            # 날짜 정보만 추출
            pubdate_date = pubdate_dt.date()
            item['pubdate'] = pubdate_date
            # 검색 결과 태그 삭제
            item['title'] = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            news_serializer = NewsSerializer(data=item)
            if news_serializer.is_valid(raise_exception=True):
                news_serializer.save()
        return JsonResponse({'message': 'okay'})

    # API 요청 실패 시 처리
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    # 기타 예외 처리
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# DB에 저장된 뉴스 정보 응답
@api_view(['GET'])
def news_data(request, code):
    try:
        # 모든 뉴스 데이터
        if code == 0:
            news_instances = News.objects.all()

        # 메인 페이지용 뉴스 데이터(5개)
        elif code == 1:
            news_instances = News.objects.all()[:5]
        
        news_serializer = NewsSerializer(news_instances, many=True)
        return Response(news_serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)