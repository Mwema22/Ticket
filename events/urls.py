from django.urls import path
from events.views import create_event_view,get_user_events_view, event_detail_view, events_list_view

urlpatterns = [
    path('create/event/', create_event_view, name="create_event"),
    path('get/user/events/', get_user_events_view, name="my_events_view"),
    path('event/<int:event_id>/', event_detail_view, name='event_detail'),
    path('events/', events_list_view, name='events_list'),


]