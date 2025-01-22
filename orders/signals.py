from django.dispatch import Signal
from .events import send_event_to_broker
import logging

# Инициализация логгера для событий
logger = logging.getLogger('events')

# Определяем сигналы
order_created = Signal()
order_updated = Signal()
order_deleted = Signal()

def handle_order_created(sender, order, **kwargs):
    try:
        event_data = {
            "order_id": order.id,
            "status": order.status,
            "customer_name": order.customer_name,
            "total_price": float(order.total_price),
        }
        send_event_to_broker("OrderCreated", event_data)
        logger.info(f"OrderCreated event sent: {event_data}")
    except Exception as e:
        logger.error(f"Error sending OrderCreated event: {e}")

def handle_order_updated(sender, order, old_status, new_status, **kwargs):
    try:
        event_data = {
            "order_id": order.id,
            "old_status": old_status,
            "new_status": new_status,
            "customer_name": order.customer_name,
            "total_price": float(order.total_price),
        }

        # Отправляем событие брокеру
        send_event_to_broker("OrderUpdated", event_data)

        # Логируем отправленное событие
        logger.info(f"OrderUpdated event sent: {event_data}")
    except Exception as e:
        logger.error(f"Error sending OrderUpdated event: {e}")

def handle_order_deleted(sender, order, **kwargs):
    try:
        event_data = {
            "order_id": order.id,
            "customer_name": order.customer_name,
        }
        send_event_to_broker("OrderDeleted", event_data)
        logger.info(f"OrderDeleted event sent: {event_data}")
    except Exception as e:
        logger.error(f"Error sending OrderDeleted event: {e}")

# Подключение сигналов
order_created.connect(handle_order_created)
order_updated.connect(handle_order_updated)
order_deleted.connect(handle_order_deleted)

