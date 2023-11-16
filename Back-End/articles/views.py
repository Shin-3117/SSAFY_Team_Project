from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer
from .models import Article, Comment
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def article_view(request, article_id=None):
    if request.method == 'GET':
        # GET 요청은 인증 요구 X
        pass
    else:
        # POST, PUT, PATCH, DELETE 요청은 인증 요구
        if not request.user.is_authenticated:
            return Response({"message": "Unauthorized"}, status=401)

    if request.method == 'GET':
        if article_id:
            article = get_object_or_404(Article, pk=article_id)
            serializer = ArticleSerializer(article)
        else:
            articles = get_list_or_404(Article)
            serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method in ['PUT', 'PATCH']:
        article = get_object_or_404(Article, pk=article_id)
        if request.user != article.user:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        article = get_object_or_404(Article, pk=article_id)
        if request.user != article.user:
            return Response({"message": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_view(request, article_id=None, comment_id=None):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method in ['PUT', 'PATCH']:
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user != comment.user:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user != comment.user:
            return Response({"message": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user = request.user

    if user in article.like_users.all():
        # 이미 '좋아요'를 눌렀다면 '좋아요' 제거
        article.like_users.remove(user)
        return Response({'status': 'like removed'})
    else:
        # '좋아요'를 누르지 않았다면 '좋아요' 추가
        article.like_users.add(user)
        return Response({'status': 'like added'})
