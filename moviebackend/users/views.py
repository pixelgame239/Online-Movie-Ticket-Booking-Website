from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UserRegisterForm, UserUpdateForm
from movies.models import Cinema, Movie
from django.core.mail import EmailMessage

@login_required
def home(request):
    movies_now_showing = Movie.objects.all().order_by('-release_date')[:6]
    movies_hot = Movie.objects.all().order_by('?')[:6]  
    return render(request, 'index.html', {
        'movies_now_showing': movies_now_showing,
        'movies_hot': movies_hot,
    })


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True  
            user.is_staff = False   
            user.is_superuser = False 
            user.save()
            messages.success(request, "Tạo tài khoản thành công!")
            
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    
    return render(request, "register.html", {"form": form})

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
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu")
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)  # thêm request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật tài khoản thành công!")
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    cinemas = Cinema.objects.all()
    return render(request, 'profile_edit.html', {
        'form': form,
        'cinemas': cinemas,
        'avatar': request.user.avatar.url if request.user.avatar else None, 
    })

def send_html_email():
    subject = 'HTML Email from Django'
    message = 'This is a <b>HTML</b> email sent using Django.'
    from_email = '20221580@eaut.edu.vn'
    recipient_list = ['20221580@eaut.edu.vn']
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()
