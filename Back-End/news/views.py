from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import requests

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
        'sort': 'date',
        'display': 100,
    }
    response = requests.get(url, headers=headers, params=params).json()
    return Response(response)


# @api_view(['GET'])
# def save_news(request):
#     try:
#         url = URL
#         headers = {
#             'X-Naver-Client-Id': API_ID,
#             'X-Naver-Client-Secret': API_SECRET
#         }
#         params = {
#             'query': '경제뉴스',
#             'sort': 'date',
#             'display': 100,
#         }
#         response = requests.get(url, headers=headers, params=params).json()

#         items = response['items']

#         for item in items:
#             item['pubDate'] = 

#     except:
#         pass