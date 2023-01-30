import os.path

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from .permissions import IsAdminAuthPermission, IsAuthorPermission
from .models import MusicInfo, Comment, Like, Rating, Basket, Vip, History
from .serializers import PostSerializer, PostListSerializer, CommentSerializer, RatingSerializer, BasketSerializer, \
    VipSerializer, HistorySerializer
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

    # @action(['POST'], detail=True)

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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['comment', 'created_at']
    ordering_fields = ['created_at', 'comment']

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
from django.http import HttpResponse, Http404


class StreamingFileAuthorView(APIView):
    """ Воспроизведение трека автора
    """
    permission_classes = [MusicInfo]

    def get(self, request):
        self.music = get_object_or_404(models.Track, user=request.user)
        if os.path.exists(self.music.file.path):
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.music.file.name}"
            return response
        else:
            return Http404


class BasketView(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


class VipView(ModelViewSet):
    queryset = Vip.objects.all()
    serializer_class = VipSerializer


class HistoryView(ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

