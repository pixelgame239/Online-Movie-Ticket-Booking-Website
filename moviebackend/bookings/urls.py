from django.urls import path
from . import views

urlpatterns = [
    path('select_seats/<int:showtime_id>/', views.select_seats, name='select_seats'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('history/', views.booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
