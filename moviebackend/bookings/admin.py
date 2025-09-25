from django.contrib import admin
from .models import Seat, Booking


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'showtime', 'seat_number', 'is_booked')
    list_filter = ('showtime', 'is_booked')
    search_fields = ('seat_number', 'showtime__movie__title', 'showtime__cinema__name')
    ordering = ('showtime', 'seat_number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'showtime', 'status', 'booking_date', 'seats_booked', 'total_price', 'payment_method', 'customer_name', 'customer_phone')
    list_filter = ('status', 'showtime__movie', 'showtime__cinema')
    search_fields = ('customer__username', 'showtime__movie__title', 'showtime__cinema__name')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date', 'total_price')  # Tự động set, không cho sửa