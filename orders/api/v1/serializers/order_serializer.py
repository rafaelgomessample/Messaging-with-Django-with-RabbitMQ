from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'product', 'created_at', 'updated_at', 'status', 'status_payment'
        ]


class OrderCreateSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        fields = ['product']
