from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class Users(AbstractUser):
    USERTYPES = [
        ('Atendee', 'Atendee'),
        ('EventPlanner', 'EventPlanner'),
        ('Admin', 'Admin'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+\d{1,3}\d{9}$}',
        message = "Phone number must start with '+' followed by country code and 9 digits."
    )

    username = models.CharField(max_length=30, unique=True) # Removed null=True
    firstname = models.CharField(max_length=30, null=True, blank=True)
    lastname = models.CharField(max_length=30, null=True, blank=True)  
    email = models.EmailField(max_length=254, unique=True) 

    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],
        null=True,
        blank=True)
    
    user_types = models.CharField(max_length=12, choices=USERTYPES, default='Atendee')
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    username_field = 'email' 
    required_field = ['username', 'firstname', 'lastname', 'phone_number'] # Fields required during user creation

    def __str__(self):
        return self.username
    

class Orders(models.Model):
    user= models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column='user',
        related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)
    order_status = models.CharField(max_length=7, default='pending')

    def __str__(self):
        return self.order_status


class Payments(models.Model):
    PAYMENT_METHOD=[
        ('Mpesa','Mpesa'),
        ('Bank Transer','Bank Transfer'),
    ]

    order = models.ForeignKey(
        Orders,
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
    payment_status = models.CharField(max_length=7, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    gateway_response_code = models.CharField(max_length=20, blank=True, null=True)
    gateway_response_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transaction_code
    

class Categories(models.Model):
    category_name = models.CharField(max_length=20, default="Music")
    icon_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name
    
class EventPlanners(models.Model):
    user= models.OneToOneField(
        Users, 
        on_delete=models.CASCADE,
        db_column='users',
        default=1
    )
    organization_name = models.CharField(max_length=20,default="Banjuka")
    description = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    organization_email = models.EmailField()
    organization_number = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    # Many-to-many relationship will be defined in Events model

    def __str__(self):
        return self.organization_name
    

class Events(models.Model):
    
    # Changed from ForeignKey to ManyToManyField for many-to-many relationship
    planners = models.ManyToManyField(
        EventPlanners,
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
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    main_image_url = models.URLField(blank=True, null=True)
    gallery_image_url = models.URLField(blank=True, null=True)
    category= models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        db_column='category',
        related_name='event'
    )
    status = models.CharField(max_length=15, default='draft')
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

class TicketTypes(models.Model):
    TICKET_NAME=[
        ('EarlyBird','EarlyBird'),
        ('VIP','VIP'),
        ('Standard','Standard'),
    ]
    event = models.ForeignKey(
        Events,
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

class OrderItems(models.Model):
    order= models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        db_column='order',
        related_name='order_items'
    )
    ticket_type= models.ForeignKey(
        TicketTypes,
        on_delete=models.CASCADE,
        db_column='ticket_type',
        related_name='order_items'
    )
    quantity = models.IntegerField()
    price_at_purchase = models.FloatField(default=0)

    def __str__(self):
        return f'ticket_type:{self.ticket_type}, quantity:{self.quantity}'
    
class Ticket(models.Model):
    order_item = models.ForeignKey(
        OrderItems,
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
    

