from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UserRegisterForm, UserUpdateForm
from django.core.mail import EmailMessage

@login_required
def home(request):
    return render(request, 'movie_list.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            login(request, user)
            return redirect('home')  
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if(username.lower().strip()=="guest"):
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def send_html_email():
    subject = 'HTML Email from Django'
    message = 'This is a <b>HTML</b> email sent using Django.'
    from_email = '20221580@eaut.edu.vn'
    recipient_list = ['20221580@eaut.edu.vn']
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()