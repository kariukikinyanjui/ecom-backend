from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Product Service API",
        default_version='v1',
        description="Microservice handling product catalog and inventory management."
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/v1/', include('products.urls'))]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/v1/products/', include('products.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
