from django.urls import path, include
from .views import MusicViewSet, CommentView, StreamFileView, ReviewCreateView
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('stream-track/', StreamFileView.as_view()),
    path('review/', ReviewCreateView.as_view()),

]