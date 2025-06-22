from django.db import models
from users.models import User
from events.models import TicketType

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    user= models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user',
        related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)
    order_status = models.CharField(max_length=9,choices=ORDER_STATUS, default='pending')

    def __str__(self):
        return self.order_status

class OrderItem(models.Model):
    order= models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column='order',
        related_name='order_items'
    )
    ticket_type= models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE,
        db_column='ticket_type',
        related_name='order_items'
    )
    quantity = models.IntegerField()
    price_at_purchase = models.FloatField(default=0)

    def __str__(self):
        return f'ticket_type:{self.ticket_type}, quantity:{self.quantity}'
    
