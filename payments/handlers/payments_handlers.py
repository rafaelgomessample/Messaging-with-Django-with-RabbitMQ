from time import sleep
from core.messaging.publisher import EventPublisher
from core.messaging.exchanges import ExchangeEnum
from orders.models.order_model import Order


def payment_notification_handler(payload: dict):
    print("Payment notification received")
    print(f"Notification send to order - {payload["order_id"]}")
    print(f"Notification type: {payload["type_notification"]}")


def payment_change_status_handler(payload: dict):
    order_id =  payload["order_id"]
    status_next =  payload["status_next"]

    print("Payment change status received")
    print(f"Order id - {order_id} to next status {status_next}")

    order = Order.objects.get(id=order_id)
    order.status_payment = status_next
    order.save()

    print("\nSend event notification from payment change status")
    event_publisher_payment_change_status_notification = EventPublisher(
        exchange=ExchangeEnum.PAYMENTS,
    )
    event_publisher_payment_change_status_notification.publish(
        routing_key="payments.payment_notification",
        payload={"order_id": order_id, "type_notification": "payment_change_status"},
    )
