import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(filed_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.NumberFilter(field_name="categories__id")

    class Meta:
        model = Product
        fields = {
            'stock': ['exact', 'gte', 'lte'],
            'is_active': ['exact'],
        }
