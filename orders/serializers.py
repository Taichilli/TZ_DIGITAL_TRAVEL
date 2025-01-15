from rest_framework import serializers
from .models import Order, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            order.products.add(product)
        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', None)
        if products_data:
            instance.products.clear()
            for product_data in products_data:
                product, _ = Product.objects.get_or_create(**product_data)
                instance.products.add(product)

        # Обновление других полей заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

