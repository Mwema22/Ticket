from django.shortcuts import render

# Create your views here.
def payments(request):
    return render(request, 'payments.html')  # Render the payments.html template
