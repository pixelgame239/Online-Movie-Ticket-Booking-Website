from django.contrib import admin
from .models import Seat, Booking
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'showtime', 'seat_number', 'is_booked')
    list_filter = ('showtime', 'is_booked')
    search_fields = ('seat_number', 'showtime__movie__title', 'showtime__cinema__name')
    ordering = ('showtime', 'seat_number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'showtime', 'status', 'booking_date', 'seats_booked', 'total_price', 'payment_method', 'customer_name', 'customer_phone', 'customer_email')
    list_filter = ('status', 'showtime__movie', 'showtime__cinema')
    search_fields = ('customer__username', 'showtime__movie__title', 'showtime__cinema__name')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date', 'total_price', 'customer_name', 'customer_phone', 'customer_email', 'payment_method', 'seats_booked', 'showtime', 'customer')  # Tự động set, không cho sửa
    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Booking.objects.get(pk=obj.pk)
            old_status = old_obj.status
            new_status = obj.status

            # Only send email if status changes from 'pending' to 'confirmed'
            if old_status == 'pending' and new_status == 'confirmed':
                self.send_confirmation_booking(obj, request)

        super().save_model(request, obj, form, change)

    def send_confirmation_booking(self, booking, request):
        subject = "Your booking is confirmed"
        domain = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        my_tickets_url = f"{protocol}://{domain}{reverse('bookings:my_tickets')}"
        message = render_to_string('booking_confirmed_email.html',{
            "booking": booking,
            'my_tickets_url': my_tickets_url,
        })
        email = EmailMessage(subject, message, '20221580@eaut.edu.vn', [booking.customer_email])
        email.content_subtype = 'html'  # This ensures the email is sent as HTML
        email.send()