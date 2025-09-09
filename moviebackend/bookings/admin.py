from django.contrib import admin
from .models import Seat, Booking, Payment

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'seat_number', 'is_booked')
    list_filter = ('showtime', 'is_booked')
    search_fields = ('seat_number', 'showtime__movie__title')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'showtime', 'status', 'booking_date', 'total_price')
    list_filter = ('status', 'showtime__movie', 'showtime__cinema')
    search_fields = ('customer__username', 'showtime__movie__title', 'showtime__cinema__name')
    filter_horizontal = ('seats',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'method', 'amount', 'status', 'payment_date')
    list_filter = ('status', 'method')
    search_fields = ('booking__customer__username',)
