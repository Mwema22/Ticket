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
            return redirect('ticket')
           
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()

    return render(request, "create_events.html", {"form": form})
    
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

def event_detail_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    tickets = event.ticket_types.all()
    return render(request, 'event_detail.html', {
        'event': event,
        'tickets': tickets
    })

def events_list_view(request):
    events = Event.objects.filter(id__isnull=False)  # Add more filters if needed
    return render(request, 'event_list.html', {'events': events})
