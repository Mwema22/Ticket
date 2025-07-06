from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import EventPlanner
from events.models import Event
from django.db.models import Q
from events.forms import EventForm

@login_required(login_url='/login/')
def create_event_view(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        planner = EventPlanner.objects.get(user=request.user)

        
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = planner 
            event.save()

            event.planners.add(planner)

            messages.success(request, 'Event created successfully!')
            return redirect('event_planner_dashboard')
           
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()

    return render(request, "create_events.html", {"form": form})


@login_required(login_url='/login/')
def my_events_view(request):
    # Get the logged-in user's EventPlanner profile
    event_planner = get_object_or_404(EventPlanner, user=request.user)

    # Filter events where the current planner is among the planners (ManyToMany)
    my_events = Event.objects.filter(planners=event_planner)

    context = {
        'my_events': my_events
    }
    return render(request, 'main/my_events.html', context)

@login_required(login_url='/login/')
def get_user_events_view(request):
    # Get the logged-in user's EventPlanner profile
    event_planner = get_object_or_404(EventPlanner, user=request.user)

    # Filter events where the current planner is among the planners (ManyToMany)
    my_events = Event.objects.filter(planners=event_planner)

    context = {
        'my_events': my_events
    }
    return render(request, 'my_events.html', context)