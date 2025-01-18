from rest_framework import serializers
from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # Поле products для отображения данных (только чтение)
    products = ProductSerializer(many=True, read_only=True)
    # Поле для записи продуктов (список ID)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), write_only=True
    )

    class Meta:
        model = Order
        fields = ['order_id', 'customer_name', 'status', 'total_price', 'products', 'product_ids']

    def create(self, validated_data):
        # Извлекаем список ID продуктов
        product_ids = validated_data.pop('product_ids', [])
        # Создаём заказ
        order = Order.objects.create(**validated_data)
        # Связываем продукты с заказом
        order.products.set(product_ids)
        return order

    def update(self, instance, validated_data):
        # Обновляем связанные продукты, если переданы
        product_ids = validated_data.pop('product_ids', None)
        if product_ids is not None:
            instance.products.set(product_ids)

        # Обновляем остальные поля заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
