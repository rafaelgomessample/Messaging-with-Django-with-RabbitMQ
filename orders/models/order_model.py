from django.db import models


class Order(models.Model):
    product = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('cancelled', 'Cancelled'),
            ('finished', 'Finished')
        ],
    )
    status_payment = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
            ('reversed', 'Reversed'),
        ],
    )

    def __str__(self):
        return (
            f"Order {self.id} - {self.product} - {self.status} - {self.status_payment}"
        )
