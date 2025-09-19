from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UserRegisterForm, UserUpdateForm



@login_required
def home(request):
    return render(request, 'movie_list.html')

from datetime import date

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Lấy dữ liệu ngày sinh từ select
            day = request.POST.get('day')
            month = request.POST.get('month')
            year = request.POST.get('year')
            if day and month and year:
                try:
                    user.birth_date = date(int(year), int(month), int(day))
                except ValueError:
                    user.birth_date = None  # tránh lỗi ngày không hợp lệ

            # Lấy giới tính
            gender = request.POST.get('gender')
            if gender in ['M', 'F']:
                user.gender = gender

            user.save()

            messages.success(request, "Account created successfully!")
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'days': range(1, 32),
        'months': range(1, 13),
        'years': range(1950, 2026),
    }
    return render(request, 'register.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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
