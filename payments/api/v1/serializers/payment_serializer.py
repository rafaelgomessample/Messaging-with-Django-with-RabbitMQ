from rest_framework import serializers

from orders.models import Order
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'created_at', 'status_old', 'status_next'
        ]

    order_id = serializers.PrimaryKeyRelatedField(
        source='order',
        queryset=Order.objects.all(),
        required=True,
    )


class PaymentCreateSerializer(PaymentSerializer):
    class Meta(PaymentSerializer.Meta):
        fields = ['order_id', 'status_next']

    order_id = serializers.PrimaryKeyRelatedField(
        source='order',
        queryset=Order.objects.filter(status='pending', status_payment='pending'),
        required=True,
    )

    def create(self, validated_data):
        order = validated_data["order"]

        validated_data["status_old"] = order.status_payment

        return super().create(validated_data)
