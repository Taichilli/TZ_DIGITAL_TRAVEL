from rest_framework import serializers
from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # Используем PrimaryKeyRelatedField для работы с продуктами через их IDs
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True)
    product_details = ProductSerializer(source='products', many=True,
        read_only=True)  # Для отображения деталей продуктов
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['order_id', 'customer_name', 'status', 'total_price', 'products', 'product_details', 'deleted', 'user']

    def create(self, validated_data):
        #Создание заказа с привязкой продуктов по их ID.
        print("Validated data",validated_data) #для отладки
        products = validated_data.pop('products', [])
        print("Products:",products) #для отладки
        order = Order.objects.create(user=self.context['request'].user,**validated_data)
        order.products.set(products)  # Привязываем продукты к заказу
        return order

    def update(self, instance, validated_data):
        # Обновляем заказа и связанных продуктов
        products = validated_data.pop('products', None)
        if products is not None:
            instance.products.set(products)

        # Обновляем остальные поля заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
