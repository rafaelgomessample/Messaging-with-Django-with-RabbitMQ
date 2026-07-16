from rest_framework import mixins, viewsets
from orders.api.v1.serializers.order_serializer import (
    OrderSerializer,
    OrderCreateSerializer,
)
from core.messaging.publisher import EventPublisher
from core.messaging.exchanges import ExchangeEnum


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = []
    authentication_classes = []
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderSerializer.Meta.model.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save()

        event_publisher_order_created = EventPublisher(exchange=ExchangeEnum.ORDERS)
        event_publisher_order_created.publish(
            routing_key="orders.order_created",
            payload={
                "order_id": serializer.instance.id,
                "status": serializer.instance.status,
                "status_payment": serializer.instance.status_payment,
                "product": serializer.instance.product,
                "created_at": str(serializer.instance.created_at),
            },
        )
