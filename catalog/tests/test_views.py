from rest_framework.test import APITestCase
from catalog.models import *
from django.urls import reverse 


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category(name= 'toiletries')
        self.category.save()

    def test_retrieve_category(self):
        self.url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.category.name)

    def test_create_category(self):
        self.url = reverse('category-list')
        data = {"name": "Books"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_category(self):
        url = reverse("category-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        data = response.data['results']
        self.assertEqual(data[0]['name'],  self.category.name)

    def test_delete_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)

    def test_update_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.pk})
        data = {"name": "Computers"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Computers")



class ProductAPITestCase(APITestCase):
    
    def setUp(self):
        self.category = Category(name = 'electronics')
        self.category.save()
        self.product1 = Product(sku ='', name='Iphone', description='', price=24.00, category=self.category)
        self.product1.save()

    def test_list_category(self):
        url = reverse("product-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        data = response.data['results']
        self.assertEqual(data[0]['name'],  self.product1.name)
    
    def test_retrieve_product(self):
        self.url = reverse('product-detail', kwargs={'sku': self.product1.sku})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.product1.name)
