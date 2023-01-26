from django.urls import path, include
from .views import MusicViewSet, CommentView, StreamFileView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('music', MusicViewSet)
router.register('comment', CommentView)
# router.register('image', ImageView)


urlpatterns = [
    path('', include(router.urls)),
    path('stream-track/', StreamFileView.as_view())
]