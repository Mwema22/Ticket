from django.shortcuts import render
from orders.models import *
# Create your views here.


def order(request):
    return render(request, 'orders.html')


