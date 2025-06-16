from django.urls import path
from  app.views import login_view, signup_view, home, event_planner_dashboard, \
create_event_view, my_events_view, get_user_events_view

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_view, name="login"),
    path('register/',signup_view, name="register"),
    path('event-planner/dashboard/', event_planner_dashboard, name="event_planner_dashboard"),
    path('create/event/', create_event_view, name="create_event_view"),
    path('get/user/events/', get_user_events_view, name="my_events_view")

]

from app.models import Users, EventPlanners

# Replace with a real username or email from your custom user model
user = Users.objects.get(username='salma')

# Now check if this user has a corresponding EventPlanners profile
EventPlanners.objects.filter(user=user).exists()
