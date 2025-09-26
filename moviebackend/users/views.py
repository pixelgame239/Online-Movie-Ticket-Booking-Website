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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import password_validators_help_texts
from django.http import Http404, HttpResponse
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from utils.supabase import upload_to_supabase
import os

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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Kiểm tra username "guest" (cấm đăng nhập)
        if username.lower() == "guest":
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không hợp lệ")
            return render(request, 'login.html')

        # Xác thực user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Chào mừng {user.username}!")
            return redirect('home')  # Hoặc URL trang chủ
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu")

    return render(request, 'login.html')
def send_password_reset_email(user, request):
    subject = 'Khôi phục mật khẩu của bạn'
    
    # Generate UID and token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Build reset link
    domain = get_current_site(request).domain
    path = reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    reset_url = f"http://{domain}{path}"

    # Render email HTML template
    message = render_to_string('forget_password_email.html', {
        'user': user,
        'reset_url': reset_url,
    })

    # Send email
    email = EmailMessage(subject, message, '20221580@eaut.edu.vn', [user.email])
    email.content_subtype = 'html'  # Send as HTML
    email.send()
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Mật khẩu đã được đặt lại thành công.')
            return redirect('users:user_login')
        return render(request, 'password_reset_form.html', {'user': user})
    else:
        return HttpResponse('Liên kết không hợp lệ hoặc đã hết hạn.')
def forget_password(request):
    if request.method=="POST":
        username = request.POST['username']
        if(username=="guest"):
            messages.error(request, 'Tên đăng nhập không tồn tại.')
            return render(request, 'forget_password.html')
        try:
            user = User.objects.get(username=username)
            if user.email:
                send_password_reset_email(user, request)
                messages.success(request, 'Liên kết đặt lại mật khẩu đã được gửi đến email của bạn.')
            else:
                messages.error(request, 'Người dùng không có email đăng ký.')
        except User.DoesNotExist:
            messages.error(request, 'Tên đăng nhập không tồn tại.')
        return redirect('users:forget_password')
    return render(request, 'forget_password.html')

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
            user = form.save(commit=False)
            avatarFile = request.FILES.get('upload_avatar')
            avatarBytes = avatarFile.read() if avatarFile else None
            if avatarFile:
                ext = os.path.splitext(avatarFile.name)[1]
                fileName = f"{request.user.username}{ext}"
                print(avatarFile)
                try:
                    avatarUrl = upload_to_supabase(avatarBytes, path_in_bucket=fileName, bucket_name="avatar")
                    user.avatar = avatarUrl
                except Exception as e:
                    messages.error(request, f"Lỗi upload ảnh đại diện {e}")
                    return redirect('users:profile_edit')
            user.save()
            messages.success(request, "Cập nhật tài khoản thành công!")
            return redirect('users:profile')
        else:
            print("Form errors:", form.errors)
    else:
        form = UserUpdateForm(instance=request.user)

    cinemas = Cinema.objects.all()
    return render(request, 'profile_edit.html', {
        'form': form,
        'cinemas': cinemas,
        'avatar': request.user.avatar if request.user.avatar else None, 
    })
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # tránh logout sau khi đổi pass
            messages.success(request, "Mật khẩu đã được thay đổi thành công!")
            return redirect('users:password_change')
        else:
            messages.error(request, "Đổi mật khẩu thất bại. Vui lòng kiểm tra lại thông tin.")
    else:
        form = PasswordChangeForm(user=request.user)
    password_requirements = password_validators_help_texts()

    return render(request, 'password_change.html', {'form': form})