from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UserRegisterForm, UserUpdateForm
from movies.models import Cinema, Movie
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404

@login_required
def home(request):
    movies_now_showing = Movie.objects.all().order_by('-release_date')[:6]
    movies_hot = Movie.objects.all().order_by('?')[:6]  
    return render(request, 'index.html', {
        'movies_now_showing': movies_now_showing,
        'movies_hot': movies_hot,
    })
def confirm_account(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activate the user account
            user.save()

            # Optionally log the user in immediately after activation
            login(request, user)
            messages.success(request, "Your account has been confirmed successfully.")
            return redirect("home")  # Redirect to a page after successful activation
        else:
            raise Http404("Invalid token")
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        raise Http404("Invalid link")
    
def send_confirmation_email(user, request):
    subject = 'Confirm Your Account'
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode())
    domain = get_current_site(request).domain
    link = reverse('users:confirm_account', kwargs={'uidb64': uid, 'token': token})
    confirm_url = f"http://{domain}{link}"
    message = render_to_string(
        'confirmation_email.html',
        {
            'user': user,
            'confirm_url': confirm_url,
        }
    )
    email = EmailMessage(subject, message, '20221580@eaut.edu.vn', [user.email])
    email.content_subtype = 'html'  # This ensures the email is sent as HTML
    email.send()


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        mess = None
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True  
            user.is_superuser = False 
            user.is_active = False
            user.save()
            send_confirmation_email(user,request)
            messages.success(request, "Hãy kiểm tra hộp thư của bạn để xác nhận tài khoản")
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