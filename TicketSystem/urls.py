"""
URL configuration for TicketSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools_stats/',include('admin_tools_stats.urls')),
    path('',include('users.urls')),
    path('',include('orders.urls')),
    path('',include('events.urls')),
    path('',include('payments.urls')),
    path('',include('tickets.urls')),
    path("", include("django.contrib.auth.urls")),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), 
         name="reset_password_done"),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="reset_password_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), 
         name="reset_password_complete"),


    
]
