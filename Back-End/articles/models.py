from django.db import models
from django.conf import settings

# Create your models here.
# 게시글 테이블
class Article(models.Model):
    # 작성자 왜래키로 지정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 좋아요 누른 사용자들
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    # 제목
    title = models.CharField(max_length=100)
    # 내용
    content = models.TextField()
    # 작성일
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정일
    updated_at = models.DateTimeField(auto_now=True)


# 댓글 테이블
class Comment(models.Model):
    # 댓글이 작성된 게시글 왜래키로 지정
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    # 작성자 왜래키로 지정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 내용
    content = models.TextField()
    # 작성일
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정일
    updated_at = models.DateTimeField(auto_now=True)
    # 대댓글(자기 자신 왜래키로 지정)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')