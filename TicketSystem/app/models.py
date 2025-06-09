from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    USERTYPES = [
        ('Atendee', 'Atendee'),
        ('EventPlanner', 'EventPlanner'),
        ('Admin', 'Admin'),
    ]

    username = models.CharField(max_length=30, unique=True) # Removed null=True
    firstname = models.CharField(max_length=30, null=True, blank=True) # Removed unique=True
    lastname = models.CharField(max_length=30, null=True, blank=True)   # Removed unique=True
    email = models.EmailField(max_length=254, unique=True) # Added unique=True for email
    # password field is handled by AbstractUser, so no explicit declaration needed here unless customizing
    phone_number = models.CharField(max_length=20, null=True, blank=True) # Increased max_length, added null/blank for flexibility
    user_types = models.CharField(max_length=12, choices=USERTYPES, default='Atendee')
    profilePicture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    USERNAME_FIELD = 'email' # Set email as the primary login field
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname', 'phone_number'] # Fields required during user creation

    def __str__(self):
        return self.username
    

class Orders(models.Model):
    user= models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column='userId',
        related_name='orders'
    )
    orderDate = models.DateTimeField(auto_now_add=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    orderStatus = models.CharField(max_length=7, default='pending')

    def __str__(self):
        return self.orderStatus


class Payments(models.Model):
    PaymentMethod=[
        ('Mpesa','Mpesa'),
        ('Bank Transer','Bank Transfer'),
    ]

    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        db_column='orderId',
        related_name='payments'
    )
    transactionCode = models.CharField(max_length=200, unique=True)
    paymentMethod = models.CharField(
        max_length=20,
        choices=PaymentMethod
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='KES')
    paymentStatus = models.CharField(max_length=50, default='pending')
    paymentDate = models.DateTimeField(auto_now_add=True)
    gatewayResponseCode = models.CharField(max_length=50, blank=True, null=True)
    gatewayResponseMessage = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transactionCode
    

class Categories(models.Model):
    categoryName = models.CharField(max_length=100)
    iconUrl = models.URLField(blank=True, null=True)
    displayOrder = models.IntegerField(default=0)

    def __str__(self):
        return self.categoryName
    
class EventPlanners(models.Model):
    userId = models.OneToOneField(
        Users, 
        on_delete=models.CASCADE,
        db_column='userId'
    )
    organizationName = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    websiteUrl = models.URLField(blank=True, null=True)
    organizationEmail = models.EmailField()
    organization_number = models.CharField(max_length=50, blank=True, null=True)
    joinDate = models.DateTimeField(auto_now_add=True)
    # Many-to-many relationship will be defined in Events model

    def __str__(self):
        return self.organizationName
    

class Events(models.Model):
    
    # Changed from ForeignKey to ManyToManyField for many-to-many relationship
    planners = models.ManyToManyField(
        EventPlanners,
        related_name='events',
        blank=True
    )
    eventName = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    venueName = models.CharField(max_length=200)
    venueAddress = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    mainImageUrl = models.URLField(blank=True, null=True)
    galleryImageUrl = models.URLField(blank=True, null=True)
    category= models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        db_column='category',
        related_name='events'
    )
    status = models.CharField(max_length=50, default='draft')
    isFeatured = models.BooleanField(default=False)
    isTrending = models.BooleanField(default=False)
    viewCount = models.IntegerField(default=0)
    creationDate = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.eventName

class TicketTypes(models.Model):
    TicketName=[
        ('EarlyBird','EarlyBird'),
        ('VIP','VIP'),
        ('Standard','Standard'),
    ]
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        db_column='eventId',
        related_name='ticket_types'
    )
    ticketName = models.CharField(
        max_length=9,
        choices=TicketName
    )
    price = models.FloatField (default=0)
    availableQty = models.IntegerField()
    soldQty = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    salesStartDate = models.DateTimeField()
    salesEndDate = models.DateTimeField()

    def __str__(self):
        return self.ticketName

class OrderItems(models.Model):
    order= models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        db_column='orderId',
        related_name='order_items'
    )
    ticketType= models.ForeignKey(
        TicketTypes,
        on_delete=models.CASCADE,
        db_column='ticketTypeId',
        related_name='order_items'
    )
    quantity = models.IntegerField()
    priceAtPurchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'ticketType:{self.ticketType}, quantity:{self.quantity}'
    
class Ticket(models.Model):
    orderItem = models.ForeignKey(
        OrderItems,
        on_delete=models.CASCADE,
        db_column='orderItemId',
        related_name='tickets'
    )
    ticketCode = models.CharField(max_length=100, unique=True)
    isScanned = models.BooleanField(default=False)
    scannedAt = models.DateTimeField(blank=True, null=True)
    issueDate = models.DateTimeField(auto_now_add=True)
    attendeeName = models.CharField(max_length=200)
    attendeeEmail = models.EmailField()

    def __str__(self):
        return f'OrderItem:{self.orderItem},ticketCode: {self.ticketCode}'
    

