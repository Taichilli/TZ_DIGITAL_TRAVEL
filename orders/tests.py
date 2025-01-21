from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Order, Product
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User



class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Создание тестового пользователя и токена
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Создание тестовых данных
        self.product1 = Product.objects.create(
            name="Product 1", price=10.0, quantity=2
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=20.0, quantity=1
        )
        self.order = Order.objects.create(
            customer_name="Test Customer",
            status="pending",
            total_price=40.0,
            user = self.user
        )
        self.order.products.set([self.product1, self.product2])

        # Настройка клиента с токеном авторизации
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_orders(self):
        response = self.client.get(reverse('orders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидаем, что будет 1 заказ
        self.assertEqual(response.data[0]['customer_name'], "Test Customer")

    def test_create_order(self):
        data = {
            "customer_name": "New Customer",
            "status": "pending",
            "total_price": 100.0,
            "products": [self.product1.id, self.product2.id]
        }
        response = self.client.post(reverse('orders-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.last().customer_name, "New Customer")

    def test_update_order(self):
        data = {
            "customer_name": "Updated Customer",
            "status": "confirmed",
            "total_price": 50.0,
            "products": [self.product1.id]
        }
        response = self.client.put(reverse('orders-detail',
            kwargs={'pk': self.order.id}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.customer_name, "Updated Customer")
        self.assertEqual(self.order.status, "confirmed")
        self.assertEqual(self.order.products.count(),1)

    def test_soft_delete_order(self):
        response = self.client.delete(
            reverse('orders-detail',kwargs={'pk': self.order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что заказ помечен как удалённый
        deleted_order = Order.all_objects.filter(pk=self.order.id).first()
        self.assertIsNotNone(deleted_order)
        self.assertTrue(deleted_order.deleted)

    def test_filter_orders(self):
        Order.objects.create(
            customer_name="Another Customer",
            status="confirmed",
            total_price=80.0,
            user=self.user
        )
        # фильтруем заказы по статусу
        response = self.client.get(reverse('orders-list') + '?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # фильтруем заказы по минимальной цене
        response = self.client.get(reverse('orders-list') + '?min_price=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

