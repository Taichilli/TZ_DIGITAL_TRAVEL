from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .signals import order_created, order_updated, order_deleted
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Фильтрация заказов только для текущего пользователя и не удалённых заказов.
        """
        # Получаем заказы только для текущего пользователя
        queryset = Order.objects.filter(user=self.request.user, deleted=False)

        # Получаем параметры фильтрации
        status = self.request.query_params.get('status')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        # Фильтрация по статусу
        if status:
            queryset = queryset.filter(status=status)

        # Фильтрация по минимальной цене
        if min_price:
            try:
                queryset = queryset.filter(total_price__gte=float(min_price))
            except ValueError:
                pass

        # Фильтрация по максимальной цене
        if max_price:
            try:
                queryset = queryset.filter(total_price__lte=float(max_price))
            except ValueError:
                pass

        return queryset
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status',openapi.IN_QUERY,description="Фильтр по статусу",
                type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Минимальная цена",
                type=openapi.TYPE_STRING),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Максимальная цена",
                type=openapi.TYPE_STRING),
        ]
    )

    def list(self, request, *args, **kwargs):
        # Уникальный ключ для кеша
        cache_key = f"orders_list_{request.user.id}"
        orders = cache.get(cache_key)

        if not orders:
            # Если кеша нет, загружаем данные из базы
            queryset = self.get_queryset()
            serializer = OrderSerializer(queryset, many=True)
            orders = serializer.data
            # сохраняем в кеш на 15 минут
            cache.set(cache_key, orders, timeout=60 * 15)

        return Response(orders)

    def perform_create(self, serializer):
        try:
            order = serializer.save()
            logger.info("order created: ", order) # Отладка
            # Отправляем сигнал
            order_created.send(sender=self.__class__, order=order)
            cache.delete(f"orders_list_{self.request.user.id}")
        except Exception as e:
            logger.error("Error during order creation:",e) # Отладка
            raise e

    def perform_update(self, serializer):
        try:
            order = serializer.save()

            # Отправляем сигнал
            order_updated.send(sender=self.__class__, order=order)
            cache.delete(f"orders_list_{self.request.user.id}")
        except Exception as e:
            raise e

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Мягкое удаление заказа
        instance.soft_delete()

        # Отправляем сигнал
        order_deleted.send(sender=self.__class__, order=instance)

        # Удаляем кеш текущего пользователя
        cache.delete(f"orders_list_{self.request.user.id}")

        return Response(status=status.HTTP_204_NO_CONTENT)
