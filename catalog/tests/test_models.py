from django.test import TestCase
from django.core.exceptions import ValidationError
from catalog.models import *



class TestCategory(TestCase):
    def setUp(self):
        self.category = Category(name='Sea foods')
        self.category.save()

    def test_slug_generation(self):
        self.assertEqual(self.category.slug, "sea-foods")


class TestProduct(TestCase):
    def setUp(self):
        self.category = Category(name = 'electronics')
        self.category.save()
        self.product1 = Product(sku ='', name='Iphone', description='', price=24.00, category=self.category)
        self.product1.save()
        

    def test_generate_sku(self):
        self.assertIsNotNone(self.product1.sku)
    

    def test_validate_price(self):
        self.product1.price = -20
        with self.assertRaises(ValidationError):
            validate_price(self.product1.price)
        


    



