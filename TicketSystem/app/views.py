from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,"main/home.html")

def login(request):
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
        
