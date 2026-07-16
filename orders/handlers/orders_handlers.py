from time import sleep
from core.messaging.publisher import EventPublisher
from core.messaging.exchanges import ExchangeEnum


def order_notification_handler(payload: dict):
    print("Order notification received")
    print(f"Notification send to order - {payload["order_id"]}")
    print(f"Notification type: {payload["type_notification"]}")


def order_created_handler(payload: dict):
    print("Order creation received")
    print(payload)

    print("\nSend event notification from order created")
    event_publisher_order_notification = EventPublisher(exchange=ExchangeEnum.ORDERS)
    event_publisher_order_notification.publish(
        routing_key="orders.order_notification",
        payload={"order_id": payload["order_id"], "type_notification": "email"},
    )

    sleep(10)
    event_publisher_payment_change_status = EventPublisher(
        exchange=ExchangeEnum.PAYMENTS
    )
    event_publisher_payment_change_status.publish(
        routing_key="payments.payment_change_status",
        payload={"order_id": payload["order_id"], "status_next": "paid"},
    )
