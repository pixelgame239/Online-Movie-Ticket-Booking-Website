from django.db import models
from django.conf import settings
from movies.models import Showtime

class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('showtime', 'seat_number')  # 1 suất chiếu chỉ có 1 ghế duy nhất

    def __str__(self):
        return f"{self.seat_number} ({'Booked' if self.is_booked else 'Available'})"


class Booking(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('momo', 'Momo'),
        ('banking', 'Banking'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    showtime = models.ForeignKey(
        Showtime,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    total_price = models.DecimalField(max_digits=7, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    quantity= models.PositiveIntegerField(help_text="Ticket quantity", default=1)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='banking')
    customer_name = models.CharField(max_length=100, null=False, blank=False, default="Guest")
    customer_phone = models.CharField(max_length=10, null=False, blank=False, default='09')

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username}"