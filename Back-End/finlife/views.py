from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
import requests
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer, DepositSerializer, SavingSerializer
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, DepositSubscription, SavingSubscription
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# custom Decorators
from .decorators import per_user_cache



# 기본 url
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# 예금 url
DEPOSIT_URL = 'depositProductsSearch.json'
# 적금 url
SAVING_URL = 'savingProductsSearch.json'
# api key
API_KEY = settings.API_KEY


# Create your views here.
# API 응답 테스트(1: 예금, 2: 적금)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_test(request, pk):
    if pk == 1:
        url = BASE_URL + DEPOSIT_URL
    elif pk == 2:
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
            # 중복 저장 방지
            if DepositProducts.objects.filter(fin_prdt_cd=product_data['fin_prdt_cd']).exists():
                continue
            # 중복이 아닌 경우에만 유효성 검사 실시 및 데이터 저장
            product_serializer = DepositProductsSerializer(data=product_data)
            if product_serializer.is_valid(raise_exception=True):
                product_serializer.save()
        
        # 옵션 데이터 저장
        for option_data in optionList:
            # 왜래키로 지정한 필드 찾기
            f_key = DepositProducts.objects.filter(fin_prdt_cd=option_data['fin_prdt_cd']).first()
            # 연관된 DepositProducts 레코드가 없는 경우 건너뜀
            if f_key is None:
                continue
            # 저축 금리 null인 경우 저장하지 않음(해당 옵션 존재하지 않는 상품)
            if option_data['intr_rate'] is None:
                continue
            # 중복 저장 방지
            if DepositOptions.objects.filter(
                intr_rate=option_data['intr_rate'],
                intr_rate2=option_data['intr_rate2'],
                save_trm=option_data['save_trm'],
                fin_prdt_cd_id=f_key.pk
            ).exists():
                continue
            # 중복이 아닌 경우에만 유효성 검사 실시 및 데이터 저장
            option_serializer = DepositOptionsSerializer(data=option_data)
            if option_serializer.is_valid(raise_exception=True):
                option_serializer.save(fin_prdt_cd=f_key)
        return JsonResponse({ 'message': 'okay' })
    
    # API 요청 실패 시 처리
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    # 기타 예외 처리
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 적금 API 요청 -> DB 저장
@api_view(['GET'])
def save_saving(request):
    try:
        url = BASE_URL + SAVING_URL
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
            # 중복 저장 방지
            if SavingProducts.objects.filter(fin_prdt_cd=product_data['fin_prdt_cd']).exists():
                continue
            # 중복이 아닌 경우에만 유효성 검사 실시 및 데이터 저장
            product_serializer = SavingProductsSerializer(data=product_data)
            if product_serializer.is_valid(raise_exception=True):
                product_serializer.save()
        
        # 옵션 데이터 저장
        for option_data in optionList:
            # 왜래키로 지정한 필드 찾기
            f_key = SavingProducts.objects.filter(fin_prdt_cd=option_data['fin_prdt_cd']).first()
            # 연관된 SavingProducts 레코드가 없는 경우 건너뜀
            if f_key is None:
                continue
            # 저축 금리 null인 경우 저장하지 않음(해당 옵션 존재하지 않는 상품)
            if option_data['intr_rate'] is None:
                continue
            # 중복 저장 방지
            if SavingOptions.objects.filter(
                intr_rate=option_data['intr_rate'],
                intr_rate2=option_data['intr_rate2'],
                save_trm=option_data['save_trm'],
                fin_prdt_cd_id=f_key.pk
            ).exists():
                continue
            # 중복이 아닌 경우에만 유효성 검사 실시 및 데이터 저장
            option_serializer = SavingOptionsSerializer(data=option_data)
            if option_serializer.is_valid(raise_exception=True):
                option_serializer.save(fin_prdt_cd=f_key)
        return JsonResponse({ 'message': 'okay' })
    
    # API 요청 실패 시 처리
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    # 기타 예외 처리
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 예금 데이터 - 저축기간 + 금리(일반, 우대) 필터에 맞게 응답
@api_view(['GET'])
# 캐싱 적용(사용자 별 캐싱 적용 완료)
@per_user_cache(60 * 15)
# @cache_page(60 * 15)
def deposit_products(request, term, sort_field):
    # 페이지네이션 적용(페이지 당 20개 데이터)
    paginator = PageNumberPagination()
    try:
        # 정렬 필드 목록(일반, 우대)
        valid_sort_fields = ['intr_rate', 'intr_rate2']

        # 입력된 정렬 필드가 유효한지 확인
        if sort_field in valid_sort_fields:
            # term이 0이면 전체 기간
            if term == 0:
                # select_related를 사용(Improve Query)
                products = DepositOptions.objects.all().select_related('fin_prdt_cd').order_by('-' + sort_field)
            else:
                # select_related를 사용(Improve Query)
                products = DepositOptions.objects.filter(save_trm=term).select_related('fin_prdt_cd').order_by('-' + sort_field)
            result_page = paginator.paginate_queryset(products, request)
            serializer = DepositSerializer(result_page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        else:
            # 유효하지 않은 정렬 필드인 경우 오류 메시지 반환
            return Response({'error': 'Invalid sort field'}, status=400)
    
    # 오류 발생 시 처리
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# 적금 데이터 - 저축기간 + 금리(일반, 우대) 필터에 맞게 응답
@api_view(['GET'])
# 캐싱 적용(사용자 별 캐싱 적용 완료)
@per_user_cache(60 * 15)
# @cache_page(60 * 15)
def saving_products(request, term, sort_field):
    # 페이지네이션 적용(페이지 당 20개 데이터)
    paginator = PageNumberPagination()
    try:
        # 정렬 필드 목록(일반, 우대)
        valid_sort_fields = ['intr_rate', 'intr_rate2']

        # 입력된 정렬 필드가 유효한지 확인
        if sort_field in valid_sort_fields:
            # term이 0이면 전체 기간
            if term == 0:
                # select_related를 사용(Improve Query)
                products = SavingOptions.objects.all().select_related('fin_prdt_cd').order_by('-' + sort_field)
            else:
                # select_related를 사용(Improve Query)
                products = SavingOptions.objects.filter(save_trm=term).select_related('fin_prdt_cd').order_by('-' + sort_field)
            result_page = paginator.paginate_queryset(products, request)
            serializer = SavingSerializer(result_page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        else:
            # 유효하지 않은 정렬 필드인 경우 오류 메시지 반환
            return Response({'error': 'Invalid sort field'}, status=400)
    
    # 오류 발생 시 처리
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# 예금 상품 구독 / 해지하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_deposit(request):
    if 'deposit_product' not in request.data or 'deposit_option' not in request.data:
        return Response({'error': 'Required data missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    deposit_product_id = request.data.get('deposit_product')
    deposit_option_id = request.data.get('deposit_option')

    subscription, created = DepositSubscription.objects.get_or_create(
        user=request.user, 
        deposit_product_id=deposit_product_id,
        deposit_option_id=deposit_option_id
    )

    if not created:  # 이미 구독 중이면 해지
        subscription.delete()
        action = 'unsubscribed'
    else:  # 구독하지 않았던 상품이면 구독
        action = 'subscribed'
    
    # 캐시 삭제 로직
    user_id = request.user.id
    page = request.data.get('page', '1')
    cache_key = f"deposit_products_{user_id}_page_{page}"
    cache.delete(cache_key)

    return Response({'action': action, 'message': f'Successfully {action}'}, status=200)


# 적금 상품 구독 / 해지하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_saving(request):
    if 'saving_product' not in request.data or 'saving_option' not in request.data:
        return Response({'error': 'Required data missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    saving_product_id = request.data.get('saving_product')
    saving_option_id = request.data.get('saving_option')

    subscription, created = SavingSubscription.objects.get_or_create(
        user=request.user,
        saving_product_id=saving_product_id,
        saving_option_id=saving_option_id
    )

    if not created:  # 이미 구독 중이면 해지
        subscription.delete()
        action = 'unsubscribed'
    else:  # 구독하지 않았던 상품이면 구독
        action = 'subscribed'

    # 캐시 삭제 로직
    user_id = request.user.id
    page = request.data.get('page', '1')
    cache_key = f"saving_products_{user_id}_page_{page}"
    cache.delete(cache_key)

    return Response({'action': action, 'message': f'Successfully {action}'}, status=200)

