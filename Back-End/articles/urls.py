from django.urls import path
from .views import article_view, comment_view, like_article

urlpatterns = [
    path('', article_view, name='article-list'),  # 게시글 목록 및 생성
    path('<int:article_id>/', article_view, name='article-detail'),  # 게시글 상세, 수정, 삭제
    path('<int:article_id>/comments/', comment_view, name='article-comments'),  # 댓글 생성
    path('comments/<int:comment_id>/', comment_view, name='comment-detail'),  # 댓글 수정, 삭제
    path('<int:article_id>/like/', like_article, name='like-article'),  # '좋아요' 기능
]
