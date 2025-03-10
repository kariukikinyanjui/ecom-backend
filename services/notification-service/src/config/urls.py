from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from notifications.views import NotificationViewSet


router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

schema_view = get_schema_view(
    openapi.Info(
        title="Notification Service API",
        default_version='v1',
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    
]
