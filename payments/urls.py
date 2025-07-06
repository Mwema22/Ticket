from django.urls import path
from payments.views import payments

urlpatterns = [
    path('payments/', payments, name='payments'),

]