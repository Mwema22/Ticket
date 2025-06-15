from django.urls import path
from  app.views import login_view, signup_view, home, event_planner_dashboard

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_view, name="login"),
    path('register/',signup_view, name="register"),
    path('event-planner/dashboard/', event_planner_dashboard, name="event_planner_dashboard"),

]