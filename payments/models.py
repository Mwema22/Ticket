from django.db import models
from orders.models import Order

# Create your models here.
class Payment(models.Model):
    PAYMENT_METHOD=[
        ('mpesa','Mpesa'),
        ('card','Card Payment'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column='order',
        related_name='payments'
    )
    transaction_code = models.CharField(max_length=15, unique=True)
    payment_method = models.CharField(
        max_length=15,
        choices= PAYMENT_METHOD
    )
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=6, default='KES')
    payment_status = models.CharField(max_length=9,choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    gateway_response_code = models.CharField(max_length=20, blank=True, null=True)
    gateway_response_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transaction_code
    