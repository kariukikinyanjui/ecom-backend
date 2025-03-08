from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Auth Service API",
        default_version='v1',
        description="Authentication Microservices API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # Add JWT security scheme configuration
    components={
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using the Bearer scheme",
            }
        }
    },
    security=[{"BearerAuth": []}],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('users.urls')),
    ])),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
