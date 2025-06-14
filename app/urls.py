from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register,name="register"),
    path('events/', views.all_events, name="events"),
    path('ticket/', views.redirect_to_default_event, name='redirect_to_default_event'),
    path('ticket/<int:event_id>/', views.ticket_page, name='ticket_page'),
    path('api/ticket-types/', views.get_ticket_types, name='get_ticket_types'),
    path('api/create-order/', views.create_order, name='create_order'),
]