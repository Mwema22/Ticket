from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_name', 'description', 'start_date', 'end_date',
            'venue_name', 'venue_address', 'city', 'country',
            'thumbnail', 'gallery_image_url', 'category',
            'status', 'is_featured', 'is_trending', 'planners','created_by'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }