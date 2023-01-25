from django.urls import path, include
from .views import MusicViewSet, CommentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('music', MusicViewSet)
router.register('comment', CommentView)


urlpatterns = [
    path('', include(router.urls))
]