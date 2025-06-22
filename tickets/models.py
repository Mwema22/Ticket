from django.db import models
from orders.models import OrderItem


# Create your models here.
class Ticket(models.Model):
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        db_column='orderItem',
        related_name='tickets'
    )
    ticket_code = models.CharField(max_length=15, unique=True)
    is_scanned = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(blank=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    attendee_name = models.CharField(max_length=20)
    attendee_email = models.EmailField()

    def __str__(self):
        return f'order_item:{self.order_item},ticket_code: {self.ticket_code}'
    

