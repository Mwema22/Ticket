from django.db import models
from django .contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    USERTYPES = [
        ('attendee', 'Attendee'),
        ('event_planner', 'Event Planner'),

    ]

    phone_regex = RegexValidator(
        regex=r'^\+\d{1,3}\d{9}$',
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
    
    user_types = models.CharField(max_length=13, choices=USERTYPES, default='attendee')
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
class EventPlanner(models.Model):
    user= models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        db_column='users',
        
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
    