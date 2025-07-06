from django.shortcuts import render

# Create your views here.
def ticket(request):
    return render(request, 'ticket.html')