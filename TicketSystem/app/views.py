from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import Users
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import *
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_GET



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
            return redirect('home')
        
        else:
            messages.error(request, 'invalid username or password')

    return render(request, 'main/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'Atendee')  # Default to Atendee
        
        # Check if user already exists
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'main/register.html')
        
        if Users.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'main/register.html')
        
        # Validate required fields
        if not all([username, firstname, lastname, email, phone_number, password]):
            messages.error(request, 'All fields are required')
            return render(request, 'main/register.html')
        
        try:
            # Create new user
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=password,
                firstname=firstname,
                lastname=lastname,
                phone_number=phone_number,
                user_types=user_type
            )
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'main/register.html')
    
    else:
        return render(request, 'main/register.html')

# Events listing view (handles /events/ URL)
def events_list(request):
    """Handle /events/ URL - redirect to all_events"""
    return all_events(request)

# 1. Main event detail view
def event_detail(request, event_id):
    """Display detailed information about a specific event"""
    event = get_object_or_404(Events, id=event_id)
    
    # Increment view count
    Events.objects.filter(id=event_id).update(view_count=F('view_count') + 1)
    
    # Get event planners
    planners = event.planners.all()
    
    # Get related events (same category, exclude current event)
    related_events = Events.objects.filter(
        category=event.category,
        status='published'
    ).exclude(id=event_id)[:4]
    
    # Get all categories for sidebar
    categories = Categories.objects.all()
    
    context = {
        'event': event,
        'planners': planners,
        'related_events': related_events,
        'categories': categories,
    }
    
    return render(request, 'main/events.html', context)

# 2. Events by category view
def events_by_category(request, category_id):
    """Display events filtered by category"""
    category = get_object_or_404(Categories, id=category_id)
    events = Events.objects.filter(
        category=category,
        status='published'
    ).order_by('-creation_date')
    
    # Pagination
    paginator = Paginator(events, 12)  # Show 12 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'events': page_obj,
        'total_events': events.count(),
    }
    
    return render(request, 'main/events.html', context)

# 3. Search events view
def search_events(request):
    """Search events by name, description, or location"""
    query = request.GET.get('q', '')
    events = Events.objects.filter(status='published')
    
    if query:
        events = events.filter(
            Q(event_name__icontains=query) |
            Q(description__icontains=query) |
            Q(venue_name__icontains=query) |
            Q(city__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'events': page_obj,
        'total_results': events.count(),
    }
    
    return render(request, 'main/events.html', context)

# 4. Featured events view
def featured_events(request):
    """Display featured events"""
    events = Events.objects.filter(
        is_featured=True,
        status='published'
    ).order_by('-creation_date')
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'page_title': 'Featured Events',
    }
    
    return render(request, 'main/events.html', context)

# 5. Trending events view
def trending_events(request):
    """Display trending events"""
    events = Events.objects.filter(
        is_trending=True,
        status='published'
    ).order_by('-view_count', '-creation_date')
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'page_title': 'Trending Events',
    }
    
    return render(request, 'main/events.html', context)

# 6. Upcoming events view
def upcoming_events(request):
    """Display upcoming events"""
    now = timezone.now()
    events = Events.objects.filter(
        start_date__gt=now,
        status='published'
    ).order_by('start_date')
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'page_title': 'Upcoming Events',
    }
    
    return render(request, 'main/events.html', context)

# 7. Events by city view
def events_by_city(request, city_name):
    """Display events filtered by city"""
    events = Events.objects.filter(
        city__iexact=city_name,
        status='published'
    ).order_by('-creation_date')
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'city': city_name,
        'events': page_obj,
        'total_events': events.count(),
    }
    
    return render(request, 'main/events.html', context)

# 8. Event planner profile view
def planner_profile(request, planner_id):
    """Display event planner profile and their events"""
    planner = get_object_or_404(EventPlanners, id=planner_id)
    events = planner.event.filter(status='published').order_by('-creation_date')
    
    # Pagination
    paginator = Paginator(events, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'planner': planner,
        'events': page_obj,
        'total_events': events.count(),
    }
    
    return render(request, 'main/events.html', context)

# 9. Contact planner form handler
@require_http_methods(["POST"])
def contact_planner(request):
    """Handle contact planner form submission"""
    if request.method == 'POST':
        planner_id = request.POST.get('planner_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Validate required fields
        if not all([planner_id, name, email, message]):
            messages.error(request, 'All fields are required.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        try:
            planner = EventPlanners.objects.get(id=planner_id)
            
            # Here you would typically send an email to the planner
            # For now, we'll just show a success message
            messages.success(request, f'Your message has been sent to {planner.organization_name}!')
            
            # You can add email sending logic here
            # send_mail(
            #     subject=f'New inquiry from {name}',
            #     message=message,
            #     from_email=email,
            #     recipient_list=[planner.organization_email],
            # )
            
        except EventPlanners.DoesNotExist:
            messages.error(request, 'Event planner not found.')
        
        return redirect(request.META.get('HTTP_REFERER', '/'))

# 10. AJAX view for event statistics
def event_stats(request, event_id):
    """Return event statistics as JSON"""
    try:
        event = Events.objects.get(id=event_id)
        stats = {
            'view_count': event.view_count,
            'planners_count': event.planners.count(),
            'is_featured': event.is_featured,
            'is_trending': event.is_trending,
            'days_until_event': (event.start_date - timezone.now()).days if event.start_date > timezone.now() else 0
        }
        return JsonResponse(stats)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

# 11. Filter events by date range
def events_by_date_range(request):
    """Filter events by date range"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    events = Events.objects.filter(status='published')
    
    if start_date:
        events = events.filter(start_date__gte=start_date)
    if end_date:
        events = events.filter(end_date__lte=end_date)
    
    events = events.order_by('start_date')
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'total_events': events.count(),
    }
    
    return render(request, 'main/events.html', context)

# 12. Toggle event favorite (AJAX)
@csrf_exempt
def toggle_favorite(request):
    """Toggle event favorite status (for logged-in users)"""
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        
        try:
            event = Events.objects.get(id=event_id)
            # Here you would typically handle user favorites
            # For now, we'll just return success
            return JsonResponse({'status': 'success', 'message': 'Favorite toggled'})
        except Events.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# 13. Get event location data for map
def event_location_data(request, event_id):
    """Return event location data for map display"""
    try:
        event = Events.objects.get(id=event_id)
        
        if event.latitude and event.longitude:
            location_data = {
                'lat': float(event.latitude),
                'lng': float(event.longitude),
                'name': event.venue_name,
                'address': event.venue_address,
                'event_name': event.event_name
            }
            return JsonResponse(location_data)
        else:
            return JsonResponse({'error': 'Location coordinates not available'}, status=404)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

# 14. All events list view
def all_events(request):
    """Display all published events with filtering options"""
    events = Events.objects.filter(status='published').order_by('-creation_date')
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    # Filter by city if specified
    city = request.GET.get('city')
    if city:
        events = events.filter(city__iexact=city)
    
    # Get unique cities for filter dropdown
    cities = Events.objects.filter(status='published').values_list('city', flat=True).distinct()
    categories = Categories.objects.all()
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'cities': cities,
        'categories': categories,
        'selected_category': category_id,
        'selected_city': city,
        'total_events': events.count(),
    }
    
    return render(request, 'main/events.html', context)

@require_GET
def redirect_to_default_event(request):
    # Redirects /ticket to a specific event (e.g. ID = 1)
    return redirect('ticket_page', event_id=1)

@require_GET
def ticket_page(request, event_id):
    """
    Render ticket.html for the given event ID
    """
    event = get_object_or_404(Events, id=event_id)
    return render(request, 'main/ticket.html', {'event': event})

def get_ticket_types(request):
    """
    Return ticket types filtered by event_id (if provided)
    """
    event_id = request.GET.get('event_id')

    if event_id:
        ticket_types = TicketTypes.objects.filter(event_id=event_id)
    else:
        ticket_types = TicketTypes.objects.all()

    data = []
    for t in ticket_types:
        data.append({
            'id': t.id,
            'ticket_name': t.ticket_name,
            'price': t.price,
            'available_qty': t.available_qty,
            'sold_qty': t.sold_qty,
        })

    return JsonResponse({'ticket_types': data})

def create_order(request):
    """
    Create order and process payment
    """
    try:
        data = json.loads(request.body)
        cart_items = data.get('cart_items', [])
        payment_method = data.get('payment_method')
        attendee_name = data.get('attendee_name')
        attendee_email = data.get('attendee_email')
        mpesa_phone = data.get('mpesa_phone')
        
        if not cart_items or not payment_method or not attendee_name or not attendee_email:
            return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
        
        # Calculate total amount and validate tickets
        total_amount = 0
        order_items_data = []

        for item in cart_items:
            ticket_type_id = item.get('ticket_id')
            quantity = item.get('quantity', 0)

            ticket_type = TicketTypes.objects.get(id=ticket_type_id)

            if ticket_type.available_qty < quantity:
                return JsonResponse({'success': False, 'message': f"Only {ticket_type.available_qty} tickets available for {ticket_type.ticket_name}"}, status=400)

            total_price = ticket_type.price * quantity
            total_amount += total_price
            order_items_data.append({
                'ticket_type': ticket_type,
                'quantity': quantity,
                'unit_price': ticket_type.price,
                'total_price': total_price
            })

        # Create order
        order = Orders.objects.create(
            attendee_name=attendee_name,
            attendee_email=attendee_email,
            total_amount=total_amount,
            payment_method=payment_method,
            status='pending'
        )

        # Create order items and reduce stock
        for item in order_items_data:
            OrderItems.objects.create(
                order=order,
                ticket_type=item['ticket_type'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                total_price=item['total_price']
            )

            # Update ticket type availability
            ticket_type = item['ticket_type']
            ticket_type.available_qty -= item['quantity']
            ticket_type.sold_qty += item['quantity']
            ticket_type.save()

        # Simulate Payment
        payment = Payments.objects.create(
            order=order,
            payment_method=payment_method,
            phone_number=mpesa_phone,
            amount=total_amount,
            status='completed'  # This can later be updated via webhook/verification
        )

        # Generate tickets
        for item in order_items_data:
            for _ in range(item['quantity']):
                ticket_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                Ticket.objects.create(
                    order=order,
                    ticket_type=item['ticket_type'],
                    ticket_code=ticket_code
                )

        # Send confirmation email
        send_mail(
            subject='Your Ticket Order Confirmation',
            message=f'Thank you {attendee_name} for your order. Your tickets have been generated.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[attendee_email],
            fail_silently=True
        )

        return JsonResponse({'success': True, 'message': 'Order created successfully', 'order_id': order.id})

    except TicketTypes.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid ticket type selected'}, status=404)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
