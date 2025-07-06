from django.urls import path
from users.views import  index, login_view,signup_view,admin_dashboard,attendee_dashboard,\
event_planner_dashboard, logout_view, profile


urlpatterns = [
    path('', index, name="index"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name="signup"),
    path('admin/dashboard/', admin_dashboard, name="admin_dashboard"),
    path('attendees/dashboard/', attendee_dashboard, name="attendee_dashboard"),
    path('event/planner/dashboard/', event_planner_dashboard, name="event_planner_dashboard"),
    path('profile/', profile, name="profile"),
    
]