from django.test import TestCase
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient
from products.models import Product, Category
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.serializers import ProductSerializer
import pytest


# Conf test
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        password='adminpass',
        is_staff=True
    )

@pytest.fixture
def test_category():
    return baker.make('product.Category', name='Electronics')

@pytest.fixture
def test_product(test_category):
    product = baker.make(
        'products.Product',
        name='Test Product',
        price=100.00,
        sku='PROD-001',
        stock=10
    )
    product.categories.add(test_category)
    return product


# Test Models
class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            price=100.00,
            sku='PROD-001',
            stock=10
        )
        self.assertEqual(str(product), "Test Product (SKU: PROD-001)")
        self.assertTrue(product.is_active)

    def test_soft_delete(self):
        product = Product.objects.create(
            name="Delete Test",
            price=50.00,
            sku="PROD-002"
        )
        product.delete()
        self.assertFalse(Product.objects.get(pk=product.pk).is_active)


class CategoryModelTest(TestCase):
    def test_category_hierarchy(self):
        parent = Category.objects.create(name="Parent")
        child = Category.objects.create(name="Child", parent=parent)
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children.all())


# Test Views
class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            sku="PROD-001",
            stock=10
        )
        self.product.categories.add(self.category)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_product_search(self):
        url = reverse('product-search')
        response = self.client.get(url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# Test Serializers
class ProductSerializerTest(TestCase):
    def test_valid_serializer(self):
        category = Category.objects.create(name="Test Category")
        data = {
            'name': 'New Product',
            'price': 99.99,
            'sku': 'PROD-123',
            'categories': [{'category': category.id, 'is_primary': True}]
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_sku(self):
        data = {
            'name': 'Invalid SKU',
            'price': 50.00,
            'sku': 'INVALID',
            'price': 50.00,
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('sku', serializer.errors)


# Integration Tests
@pytest.mark.django_db
def test_product_creation(api_client, admin_user, test_category):
    api_client.force_authenticate(user=admin_user)
    url = '/products/'
    data = {
        'name': 'New Product',
        'price': 199.99,
        'sku': 'PROD-999',
        'categories': [{'category': test_category.id, 'is_primary': True}]
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['sku'] == 'PROD-999'

@pytest.mark.django_db
def test_bulk_operations(api_client, admin_user):
    api_client.force_authentication(user=admin_user)
    bulk_url = '/products/bulk/'

    # Bulk Create
    create_data = [{
        'name': f'Product {i}',
        'price': 100 + 1,
        'sku': f'PROD-{i}'
    } for i in range(3)]

    create_response = api_client.post(bulk_url, create_data, format='json')
    assert create_response.status_code == status.HTTP_201_CREATED

    # Bulk Update
    update_data = [{
        'id': i+1,
        'price': 200 + i
    } for i in range(3)]

    update_response = api_client.patch(bulk_url, update_data, format='json')
    assert update_response.status_code == status.HTTP_200_OK
