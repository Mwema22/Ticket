from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import EventPlanner
from events.models import Event, TicketType
from tickets.forms import TicketTypeForm

@login_required(login_url='/login/')
def create_ticket_type(request):
    planner = get_object_or_404(EventPlanner, user=request.user)
    user_events = Event.objects.filter(created_by=planner)

    if not user_events.exists():
        messages.error(request, "You must create an event before adding tickets.")
        return redirect('create_event')  # or your actual event creation URL name

    if request.method == 'POST':
        form = TicketTypeForm(request.POST)
        form.fields['event'].queryset = user_events  # ✅ set queryset here

        if form.is_valid():
            ticket_type = form.save(commit=False)
            ticket_type.save()
            messages.success(request, 'Ticket created successfully')
            return redirect('event_planner_dashboard')
        else:
            messages.error(request, 'Please correct the errors below')

    else:
        form = TicketTypeForm()
        form.fields['event'].queryset = user_events  

    return render(request, 'create_tickets.html', {'form': form})  


@login_required(login_url='/login/')
def my_tickets_view(request):
    event_planner = get_object_or_404(EventPlanner, user=request.user)
    print("Logged-in planner:", event_planner)

    my_tickets = TicketType.objects.filter(event__created_by=event_planner)
    print("Events created by this planner:", list (my_tickets))

    context = {
        'my_tickets': my_tickets
    }
    return render(request, 'my_tickets.html', context)

def ticket_list_view(request):
    events = Event.objects.prefetch_related('ticket_types').all()
    return render(request, 'ticket_list.html', {'events': events})
