from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class OrderManager(models.Manager):
    def get_queryset(self):
        # Возвращаем только записи, где deleted=False
        return super().get_queryset().filter(deleted=False)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField('Product')
    deleted = models.BooleanField(default=False)  # Для мягкого удаления

    # Менеджеры
    objects = OrderManager()  # Менеджер для активных записей
    all_objects = models.Manager()  # Менеджер для всех записей (включая удалённые)

    def soft_delete(self):
        """Мягкое удаление заказа"""
        self.deleted = True
        self.save()

    def restore(self):
        """Восстановление мягко удалённого заказа"""
        self.deleted = False
        self.save()

    def get_products_summary(self):
        """Возвращает сводку по продуктам заказа"""
        return [{"name": product.name, "quantity": product.quantity} for product in self.products.all()]

    def update_total_price(self):
        """Пересчитывает стоимость заказа на основе продуктов"""
        self.total_price = sum(product.price * product.quantity for product in self.products.all())
        self.save()

    def add_product(self, product, quantity=1):
        """Добавляет продукт в заказ с заданным количеством"""
        self.products.add(product)
        product.quantity += quantity
        product.save()
        self.update_total_price()  # Пересчитываем стоимость после добавления продукта

    def remove_product(self, product, quantity=1):
        """Удаляет продукт из заказа с заданным количеством"""
        self.products.remove(product)
        product.quantity -= quantity
        product.save()
        self.update_total_price()  # Пересчитываем стоимость после удаления продукта




