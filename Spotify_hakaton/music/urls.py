from django.urls import path, include
from .views import MusicViewSet, CommentView, StreamingFileAuthorView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('music', MusicViewSet)
router.register('comment', CommentView)
# router.register('image', ImageView)


urlpatterns = [
    path('twoandone/', include(router.urls)),
    path('stream-track/', StreamingFileAuthorView.as_view())
]