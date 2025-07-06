from django.urls import path
from events.views import create_event_view,get_user_events_view

urlpatterns = [
    path('create/event/', create_event_view, name="create_event_view"),
    path('get/user/events/', get_user_events_view, name="my_events_view"),


]