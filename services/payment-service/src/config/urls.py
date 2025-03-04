from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from payments.webhooks import stripe_webhook


schema_view = get_schema_view(
    openapi.Info(
        title="Payment Service API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payments.urls')),
    path('webhook/stripe/', stripe_webhook, name='stripe-webhook'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('metric/', include('django_prometheus.urls')),
]
