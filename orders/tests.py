from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, Product
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


def get_token():
    # Создаём пользователя, для которого будет сгенерирован токен
    user = User.objects.create_user(username="testuser", password="testpassword")

    # Генерируем токен
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)  # Возвращаем access-токен


class OrderTestCase(TestCase):
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
            total_price=40.0
        )
        self.order.products.set([self.product1, self.product2])

        # Настройка клиента с токеном авторизации
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_update_order(self):
        data = {
            "customer_name": "Updated Customer",
            "status": "confirmed",
            "total_price": 50.0,
            "products": [
                {"name": "Product 1", "price": 10.0, "quantity": 2},
                {"name": "Product 2", "price": 20.0, "quantity": 1}
            ]
        }
        response = self.client.put(
            reverse('order-detail', kwargs={'pk': self.order.order_id}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.customer_name, "Updated Customer")

    def test_get_orders(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидаем, что будет 1 заказ
        self.assertEqual(response.data[0]['customer_name'], "Test Customer")

    def test_soft_delete_order(self):
        response = self.client.delete(
            reverse('order-detail', kwargs={'pk': self.order.order_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что заказ помечен как удалённый
        deleted_order = Order.all_objects.filter(pk=self.order.order_id).first()
        self.assertIsNotNone(deleted_order)
        self.assertTrue(deleted_order.deleted)



