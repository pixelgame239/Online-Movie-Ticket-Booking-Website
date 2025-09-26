from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('confirm-account/<uidb64>/<token>/', views.confirm_account, name='confirm_account'),
    path('password-change/', views.password_change, name='password_change'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path("booking/<int:showtime_id>/", views.booking_view, name="booking"),
    path("booking/completed/", views.booking_completed, name="booking_completed"),
]
