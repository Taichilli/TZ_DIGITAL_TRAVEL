from django.dispatch import Signal
from .events import send_event_to_broker

# Определяем сигналы
order_created = Signal()
order_updated = Signal()
order_deleted = Signal()

def handle_order_created(sender, order, **kwargs):
    try:
        send_event_to_broker(
            "OrderCreated",
            {
                "order_id": order.id,
                "status": order.status,
                "customer_name": order.customer_name,
                "total_price": float(order.total_price),
            }
        )
    except Exception as e:
        print(f"Error sending OrderCreated event: {e}")

def handle_order_updated(sender, order, **kwargs):
    try:
        send_event_to_broker(
            "OrderUpdated",
            {
                "order_id": order.id,
                "status": order.status,
                "customer_name": order.customer_name,
                "total_price": float(order.total_price),
            }
        )
    except Exception as e:
        print(f"Error sending OrderUpdated event: {e}")

def handle_order_deleted(sender, order, **kwargs):
    try:
        send_event_to_broker(
            "OrderDeleted",
            {
                "order_id": order.id,
                "customer_name": order.customer_name,
            }
        )
    except Exception as e:
        print(f"Error sending OrderDeleted event: {e}")

# Подключение сигналов
order_created.connect(handle_order_created)
order_updated.connect(handle_order_updated)
order_deleted.connect(handle_order_deleted)
