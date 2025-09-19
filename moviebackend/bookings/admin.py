from django.contrib import admin
from .models import Seat, Booking, Payment, Ticket


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'showtime', 'seat_number', 'is_booked')
    list_filter = ('showtime', 'is_booked')
    search_fields = ('seat_number', 'showtime__movie__title', 'showtime__cinema__name')
    ordering = ('showtime', 'seat_number')


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'showtime', 'status', 'booking_date', 'total_price')
    list_filter = ('status', 'showtime__movie', 'showtime__cinema')
    search_fields = ('customer__username', 'showtime__movie__title', 'showtime__cinema__name')
    inlines = [TicketInline]
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date', 'total_price')  # Tự động set, không cho sửa


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'method', 'amount', 'status', 'payment_date')
    list_filter = ('status', 'method')
    search_fields = ('booking__customer__username', 'booking__showtime__movie__title')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)
    readonly_fields = ('payment_date',)  # Ngày thanh toán auto, không cho sửa


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'seat', 'price')
    list_filter = ('booking__showtime__movie',)
    search_fields = ('booking__customer__username', 'seat__seat_number')
    ordering = ('booking', 'seat')
