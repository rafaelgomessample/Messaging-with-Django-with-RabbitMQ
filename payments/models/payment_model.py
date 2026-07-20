from django.db import models


class Payment(models.Model):

    CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('reversed', 'Reversed'),
    ]

    order = models.ForeignKey(to="orders.Order", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    status_old = models.CharField(
        max_length=20,
        choices=CHOICES,
    )
    status_next = models.CharField(
        max_length=20,
        choices=CHOICES,
    )

    def __str__(self):
        return (
            f"Payment {self.id} - {self.order.product} -"
            " {self.status_old} to {self.status_next}"
        )
