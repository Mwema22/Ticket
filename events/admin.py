from django.contrib import admin
from events.models import EventCategory,Event,TicketType
# Register your models here.


admin.site.register(EventCategory)
admin.site.register(TicketType)
admin.site.register(Event)  # Register the Event model
