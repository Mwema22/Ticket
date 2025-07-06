from django.urls import path
from tickets.views import ticket

urlpatterns = [
    path('tickets/', ticket, name='ticket'),

]
