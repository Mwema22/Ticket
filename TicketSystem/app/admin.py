from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Users),
admin.site.register(Events),
admin.site.register(Categories),
admin.site.register(EventPlanners),
admin.site.register(Orders),
admin.site.register(OrderItems),
admin.site.register(Ticket),
admin.site.register(TicketTypes),
admin.site.register(Payments),

