from django import forms
from events.models import TicketType
from tickets.models import Ticket

class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = [
            'ticket_name','price','available_qty','description','sales_start_date',
            'sales_end_date','event'
        ]

        widgets = {
            'sales_start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sales_end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
