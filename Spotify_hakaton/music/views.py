import os.path

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from .permissions import IsAdminAuthPermission, IsAuthorPermission
from .models import MusicInfo, Comment, Like, Rating, Favorite
from .serializers import PostSerializer, PostListSerializer, CommentSerializer, RatingSerializer
import django_filters
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models


class MusicViewSet(ModelViewSet):
    queryset = MusicInfo.objects.all()
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['category']
    search_fields = ['slug', 'created_at']
    ordering_fields = ['created_at', 'title']

    # api/v1/posts/pk(post1)/comments
    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST', 'PATCH'], detail=True)
    def rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(
            data=data, context={'request': request}
        )
        rating = Rating.objects.filter(
            author=request.user,
            post=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('use PATCH method')
        elif rating and request.method == 'PATCH':
            serializer.update(rating, serializer.validated_data)
            return Response('UPDATED')
        elif request.method == 'POST':
            serializer.create(
                serializer.validated_data
            )
            return Response('CREATED')


    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'disliked'
            if not like.is_liked:
                like.delete()
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user, is_liked=True)
            message = 'liked'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()


# class ImageView(ModelViewSet):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             self.permission_classes = [AllowAny]
#
#         elif self.action == 'create':
#             self.permission_classes = [IsAdminAuthPermission]
#
#         elif self.action in ['update', 'partial_update', 'destroy']:
#             self.permission_classes = [IsAuthorPermission]
#
#         return super().get_permissions()
from django.http import FileResponse, Http404


class StreamFileView(APIView):

    def set_play(self, track):
        track.plays.count += 1
        track.save()

    def get(self, request, pk):
        track = get_object_or_404(MusicInfo, id=pk)
        if os.path.exists(track.file.path):
            self.set_play(track)
            return FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
        else:
            return Http404

    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(post=post, author=user)
            favorite.is_favorite = not favorite.is_favorite
            favorite.save()
            message = 'favorite' if favorite.is_favorite else 'no favorite'
            if not favorite.is_favorite:
                favorite.delete()
        except Favorite.DoesNotExist:
            Favorite.objects.create(post=post, author=user, is_favorite=True)
            message = 'favorite'
        return Response(message, status=200)
