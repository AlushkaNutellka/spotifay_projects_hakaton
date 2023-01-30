from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Joe Speen Api',
        description='Akjol',
        default_version='v1',
        public=True 
    ) 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('spotify/', include('music.urls')),
    path('docs/', schema_view.with_ui('swagger')),
    path('account/', include('account.urls')),
    path('', include('music.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)