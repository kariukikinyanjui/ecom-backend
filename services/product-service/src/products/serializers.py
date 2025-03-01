from rest_framework import serializers
from .models import Product, Category, ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'description']
        read_only_fields = ['id']


class ProductCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['category', 'is_primary']
        read_only_fields = ['category']


class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(
        many=True,
        source='productcategory_set', # Use through model relationship
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'sku', 'categories', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'sku': {'required': True}
        }

        def validate_sku(self, value):
            '''Ensure SKU follows company format (example validation)'''
            if not value.startswith('PROD-'):
                raise serializers.ValidateError("SKU must start with 'PROD-'")
            return value


class BulkProductSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ['id'] + ProductSerializer.Meta.fields
        read_only_fields = ['id']


class BulkProductUpdateSerializer(serializers.ListSerializer):
    child = BulkProductSerializer()

    def update(self, instances, validated_data):
        # Perform bulk update logic
        updated_products = []
        for instance, data in zip(instance, validated_data):
            for attr, value in data.items():
                setattr(instance, attr, value)
            updated_products.append(instance)

        Product.objects.bulk_update(updated_products, ['price', 'stock', 'is_active'])
        return updated_products
