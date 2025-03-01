from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter


class ProductListCreateView(generics.ListCreateAPIView):
    '''
    List all products or create a new product
    - Supports filtering by category, price range, and stock status
    - Supports ordering by price, creation date
    '''
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at'] # Default ordering


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    '''Detailed product operations with soft delete support'''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        '''Soft delete implementation'''
        instance.is_active = False
        instance.save()


class CategoryListCreateView(generics.ListCreateAPIView):
    '''Manage product categories with hierarchical support'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a category instance.
    - Deleting a category will orphan its children (sets parent to NULL)
    - Only admin users can modify categories (permission handled via auth-service)
    '''

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        '''Handle category deletion with child preservation'''
        children = instance.children.all()
        children.update(parent=None)
        instance.delete()
