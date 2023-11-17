from django.core.cache import cache
from functools import wraps
from rest_framework.response import Response

def per_user_cache(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 사용자 식별자 생성 (예: 사용자 ID)
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'
            cache_key = f"{view_func.__name__}_{user_id}"

            # 캐시에서 데이터 가져오기
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                # 캐시된 데이터가 있다면 Response 객체로 반환
                return Response(cached_data)
            else:
                # 캐시된 데이터가 없다면 뷰 함수 실행
                response = view_func(request, *args, **kwargs)
                # 응답 데이터를 캐시에 저장
                cache.set(cache_key, response.data, timeout)
                return response
        return _wrapped_view
    return decorator
