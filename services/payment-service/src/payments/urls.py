from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet


router = DefaultRouter()
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:order_id>/refund/',
         PaymentViewSet.as_view({'post': 'refund'}),
         name='payment-refund'),
]
