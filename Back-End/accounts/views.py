from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserDetailSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
@api_view(['GET'])
def profile_view(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
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