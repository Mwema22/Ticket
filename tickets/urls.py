from django.urls import path
from tickets.views import create_ticket_type, my_tickets_view,ticket_list_view

urlpatterns = [
    path('create_tickets/', create_ticket_type, name='ticket'),
    path('my_tickets/', my_tickets_view, name='my_ticket_view'),
    path('tickets/', ticket_list_view, name='ticket_list'),



]
