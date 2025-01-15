from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .signals import order_created, order_updated, order_deleted
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.filter(deleted=False)
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        try:
            order = serializer.save()
            # Отправляем сигнал
            order_created.send(sender=self.__class__, order=order)
        except Exception as e:
            raise e

    def perform_update(self, serializer):
        try:
            order = serializer.save()
            # Отправляем сигнал
            order_updated.send(sender=self.__class__, order=order)
        except Exception as e:
            raise e

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        # Отправляем сигнал
        order_deleted.send(sender=self.__class__, order=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

