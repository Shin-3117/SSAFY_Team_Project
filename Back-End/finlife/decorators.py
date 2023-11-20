from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response

def per_user_cache(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 사용자 식별자와 페이지 번호, URL 경로 생성
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'
            page = request.query_params.get('page', '1')
            path = request.path  # URL 경로 추가
            cache_key = f"{view_func.__name__}_{user_id}_page_{page}_path_{path}"

            # 캐시에서 데이터 가져오기
            cached_data = cache.get(cache_key)
            if cached_data is None:
                # 캐시된 데이터가 없다면 뷰 함수 실행
                response = view_func(request, *args, **kwargs)
                # 응답 데이터를 캐시에 저장
                cache.set(cache_key, response.data, timeout)
                return response
            else:
                # 캐시된 데이터가 있다면 Response 객체로 반환
                return Response(cached_data)
        return _wrapped_view
    return decorator
