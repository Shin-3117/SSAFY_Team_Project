from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests

# 기본 url
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# 예금 url
DEPOSIT_URL = 'depositProductsSearch.json'
# 적금 url
SAVING_URL = 'savingProductsSearch.json'
# api key
API_KEY = settings.API_KEY

# Create your views here.
@api_view(['GET'])
def api_test(request):
    url = BASE_URL + DEPOSIT_URL
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(url, params=params).json()
    return Response(response)