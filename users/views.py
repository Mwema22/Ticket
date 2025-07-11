from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import views as auth_views
from users.models import EventPlanner
from users.forms import RegistrationForm, UserUpdateForm
from events.models import Event, EventCategory
from django.utils import timezone
from datetime import timedelta
from events.models import Event

def index(request):
    today = timezone.localdate()
    now = timezone.now()

    # All events
    all_events = Event.objects.all().order_by('start_date')

    # Today's events
    today_events = Event.objects.filter(start_date__date=today)

    # Weekend events
    if today.weekday() in [5, 6]:  # today is Sat or Sun
        saturday = today if today.weekday() == 5 else today - timedelta(days=1)
        sunday = today if today.weekday() == 6 else today
    else:
        saturday = today + timedelta((5 - today.weekday()) % 7)
        sunday = saturday + timedelta(days=1)

    weekend_events = Event.objects.filter(start_date__date__gte=saturday, start_date__date__lte=sunday)

    # Free events
    free_events = Event.objects.filter(ticket_types__price=0).distinct()

    categories = EventCategory.objects.all().order_by('display_order')


    return render(request, 'index.html', {
        'all_events': all_events,
        'today_events': today_events,
        'weekend_events': weekend_events,
        'free_events': free_events,
        'categories': categories,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            if user.user_types == "attendee":
                return redirect("attendee_dashboard")
            elif user.user_types == "event_planner":  
                return redirect("event_planner_dashboard")
            elif user.is_superuser:
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Unauthorized access")
                return redirect("index") 
        
        else:
            messages.error(request, 'invalid username or password')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)  
    return redirect('/')


def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            if user.user_types == 'event_planner':
                EventPlanner.objects.create(user=user)

            return redirect("login") 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    
    return render(request, "signup.html", {"form": form})

@login_required(login_url='/login/')
def admin_dashboard(request):
    """Display event planner dashboard"""
    return render(request, 'admin_dashboard.html')
    

@login_required(login_url='/login/')
def attendee_dashboard(request):
    """Display event planner dashboard"""
    return render(request, 'attendees_dashboard.html')
    

@login_required(login_url='/login/')
def event_planner_dashboard(request):
    """Display event planner dashboard"""
    return render(request, 'event_planner_dashboard.html')
    
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form})
    
