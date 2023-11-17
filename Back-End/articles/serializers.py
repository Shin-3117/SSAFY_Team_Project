from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class ArticleListSerializer(serializers.ModelSerializer):
    user = Userserializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'user',)


class CommentSerializer(serializers.ModelSerializer):
    user = Userserializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)

    def get_replies(self, obj):
        # 대댓글 직렬화
        if obj.parent is not None:
            return []  # 대댓글의 대댓글은 처리하지 않음
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True, read_only=True).data


class ArticleSerializer(serializers.ModelSerializer):
    user = Userserializer(read_only=True)
    like_users = Userserializer(read_only=True, many=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = '__all__'

    def get_comments(self, obj):
        # 상위 댓글만 필터링
        top_level_comments = obj.comments.filter(parent__isnull=True)
        return CommentSerializer(top_level_comments, many=True).data


# 프로필 페이지용 댓글 시리얼라이저
class ProfileCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'article', 'user', 'content', 'created_at', 'updated_at',)
