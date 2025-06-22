from django.db import models
from users.models import EventPlanner
# Create your models here.

class EventCategory(models.Model):
    category_name = models.CharField(max_length=20, default="Music")
    icon_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name
    

class Event(models.Model):
    STATUS = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
        ('live', 'Live'),
    ]
    
    # Changed from ForeignKey to ManyToManyField for many-to-many relationship
    planners = models.ManyToManyField(
        EventPlanner,
        related_name='event',
        blank=True
    )
    event_name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue_name = models.CharField(max_length=20)
    venue_address = models.TextField()
    city = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    thumbnail = models.URLField(blank=True, null=True)
    gallery_image_url = models.URLField(blank=True, null=True)
    category= models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        db_column='category',
        related_name='event'
    )
    status = models.CharField(max_length=8, choices=STATUS, default='upcoming')
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

class TicketType(models.Model):
    TICKET_NAME=[
        ('EarlyBird','EarlyBird'),
        ('VIP','VIP'),
        ('Standard','Standard'),
    ]
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        db_column='event',
        related_name='ticket_types'
    )
    ticket_name = models.CharField(
        max_length=9,
        choices=TICKET_NAME
    )
    price = models.FloatField (default=0)
    available_qty = models.IntegerField()
    sold_qty = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    sales_start_date = models.DateTimeField()
    sales_end_date = models.DateTimeField()

    def __str__(self):
        return self.ticket_name

