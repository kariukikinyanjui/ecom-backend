from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    '''Hierarchical product categorization system'''
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    '''Core product representation with inventory tracking'''
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)] # Prevent negative prices
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)] # Prevent negative inventory
    )
    sku = models.CharField(max_length=50, unique=True) # Stock Keeping Unit
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        through='ProductCategory'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True) # For full-text search

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price', 'created_at']),
            GinIndex(fields=['search_vector'], name='search_vector_idx'),
        ]

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"


class ProductCategory(models.Model):
    '''Explicit through model for product-category relationships'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = [('product', 'category')]
