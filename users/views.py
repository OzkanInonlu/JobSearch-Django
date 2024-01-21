from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from core.models import *
# Create your views here.


#register applicants
def register_applicant(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid(): #clean method'u çalışacak
            var = form.save(commit=False)
            var.is_applicant = True
            var.username = var.email
            var.save()

            Resume.objects.create(user=var)
            messages.info(request, "Your account has been created")
            return redirect('login')

        else:
            messages.warning(request, "Something went wrong")
            return redirect('users:register_applicant')
        
    else:
        form = RegisterForm()
        return render(request, "users/register-applicant.html", {"form":form})
    

#register employers
def register_employer(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid(): #clean method'u çalışacak
            var = form.save(commit=False)
            var.is_employer = True
            var.username = var.email
            var.save()

            Company.objects.create(user=var)
            messages.info(request, "Your account has been created")

            return redirect('login')

        else:
            messages.warning(request, "Something went wrong")
            return redirect('users:register_employer')
        
    else:
        form = RegisterForm()
        return render(request, "users/register-employer.html", {"form":form})


#login user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username = email, password= password)

        if user is not None and user.is_active:
            login(request, user)
            if request.user.is_applicant:
                return redirect("core:applicant_dashboard")
            elif request.user.is_employer:
                return redirect("core:employer_dashboard")
            else:
                return redirect("users:login")
            
        else:
            messages.danger(request, "Something went wrong. Please try again.")
            return redirect("users:login")
    else:
        return render(request, "users/login.html")
    


#logout
def logout_user(request):
    logout(request)
    messages.success(request, "Your session has ended.")
    return redirect("users:login")