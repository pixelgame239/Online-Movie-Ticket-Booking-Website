from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('confirm-account/<uidb64>/<token>/', views.confirm_account, name='confirm_account'),
    path('password-change/', views.password_change, name='password_change'),
]
