from rest_framework import mixins, viewsets
from payments.api.v1.serializers.payment_serializer import (
    PaymentSerializer,
    PaymentCreateSerializer,
)
from core.messaging.publisher import EventPublisher
from core.messaging.exchanges import ExchangeEnum


class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = []
    authentication_classes = []
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return PaymentSerializer.Meta.model.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save()

        event_publisher_payment_change_status = EventPublisher(
            exchange=ExchangeEnum.PAYMENTS
        )
        event_publisher_payment_change_status.publish(
            routing_key="payments.payment_change_status",
            payload={
                "order_id": serializer.instance.order_id,
                "status_next": serializer.instance.status_next,
                "created_at": str(serializer.instance.created_at),
            },
        )
