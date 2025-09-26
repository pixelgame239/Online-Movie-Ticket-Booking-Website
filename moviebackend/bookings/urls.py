from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path('select_seats/<int:showtime_id>/', views.select_seats, name='select_seats'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('history/', views.booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my-tickets/', views.my_tickets_view, name='my_tickets'),
    path('buy_ticket/<int:movie_id>/', views.buy_ticket, name='buy_ticket'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
]
