from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserDetailSerializer, DeleteUserSerializer, UpdateUserSerializer, PasswordChangeSerializer
from django.contrib.auth import get_user_model
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


# Create your views here.
# 프로필 조회
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def profile_view(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# 팔로우
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    if request.user.pk == user_pk:
        return Response({'error': 'You cannot follow yourself.'}, status=400)
    user_to_follow = get_object_or_404(User, pk=user_pk)
    if request.user in user_to_follow.followers.all():
        user_to_follow.followers.remove(request.user)
        action = 'unfollowed'
    else:
        user_to_follow.followers.add(request.user)
        action = 'followed'
    return Response({'action': action, 'following': user_to_follow.username})


# 유저 데이터 관련
@api_view(['DELETE', 'PUT', 'POST'])
@permission_classes([IsAuthenticated])
def user_operations(request):
    # 회원탈퇴
    if request.method == 'DELETE':
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            if user.username == username and user.check_password(password):
                user.delete()
                return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            elif user.username != username:
                return Response({'error': 'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정
    elif request.method == 'PUT':
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    # 비밀번호 변경
    elif request.method == 'POST':
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(current_password):
                return Response({'current_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'status': 'password changed'})