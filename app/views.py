from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import *
from app.forms import RegistrationForm , EventForm
from app.models import EventPlanners

# Create your views here.
def home(request):
    """Display homepage with featured events"""
    featured_events = Events.objects.filter(
        is_featured=True,
        status='published'
    ).order_by('-creation_date')[:6]
    
    trending_events = Events.objects.filter(
        is_trending=True,
        status='published'
    ).order_by('-view_count')[:6]
    
    upcoming_events = Events.objects.filter(
        start_date__gt=timezone.now(),
        status='published'
    ).order_by('start_date')[:6]
    
    categories = Categories.objects.all()[:8]
    
    context = {
        'featured_events': featured_events,
        'trending_events': trending_events,
        'upcoming_events': upcoming_events,
        'categories': categories,
    }
    
    return render(request, 'main/home.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            if user.user_types == "attendee":
                return redirect("attendee-dashboard")
            elif user.user_types == "event_planner":  
                return redirect("event_planner_dashboard")
            elif user.is_superuser:
                return redirect("/admin/")
            else:
                messages.error(request, "Unauthorized access")
                return redirect("home") 
        
        else:
            messages.error(request, 'invalid username or password')

    return render(request, 'main/login.html')


def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            if user.user_types == 'event_planner':
                EventPlanners.objects.create(user=user)

            return redirect("login") 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    
    return render(request, "main/register.html", {"form": form})


def home(request):
    """Display homepage with featured events"""
    featured_events = Events.objects.filter(
        is_featured=True,
        status='published'
    ).order_by('-creation_date')[:6]
    
    trending_events = Events.objects.filter(
        is_trending=True,
        status='published'
    ).order_by('-view_count')[:6]
    
    upcoming_events = Events.objects.filter(
        start_date__gt=timezone.now(),
        status='published'
    ).order_by('start_date')[:6]
    
    categories = Categories.objects.all()[:8]
    
    context = {
        'featured_events': featured_events,
        'trending_events': trending_events,
        'upcoming_events': upcoming_events,
        'categories': categories,
    }
    
    return render(request, 'main/home.html', context)

@login_required(login_url='/login/')
def event_planner_dashboard(request):
    """Display event planner dashboard"""
    return render(request, 'main/event_planner_dashboard.html')
    

@login_required(login_url='/login/')
def create_event_view(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_planner_dashboard')  
    else:
        form = EventForm()
    return render(request, "main/create_event.html", {"form": form})

@login_required(login_url='/login/')
def my_events_view(request):
    # Get the logged-in user's EventPlanner profile
    event_planner = get_object_or_404(EventPlanners, user=request.user)

    # Filter events where the current planner is among the planners (ManyToMany)
    my_events = Events.objects.filter(planners=event_planner)

    context = {
        'my_events': my_events
    }
    return render(request, 'main/my_events.html', context)

@login_required(login_url='/login/')
def get_user_events_view(request):
    # Get the logged-in user's EventPlanner profile
    event_planner = get_object_or_404(EventPlanners, user=request.user)

    # Filter events where the current planner is among the planners (ManyToMany)
    my_events = Events.objects.filter(planners=event_planner)

    context = {
        'my_events': my_events
    }
    return render(request, 'main/my_events.html', context)