from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from reviews.analytics import ProductAnalyticsView


schema_view = get_schema_view(
    openapi.Info(
        title="Review Service API",
        default_version='v1',
        description="Product review management system",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<uuid:product_id>/reviews/', include('reviews.urls')),
    path('products/<uuid:product_id>/analytics/', ProductAnalyticsView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
