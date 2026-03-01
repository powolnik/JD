from django.test import TestCase
from store.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product description",
            price=10.00
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_product_fields(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "A test product description")
        self.assertEqual(self.product.price, 10.00)
