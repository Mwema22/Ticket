from django.urls import path
from orders.views import Order

urlpatterns =[
    path('orders/',Order,name='orders'),
]