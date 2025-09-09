from django.db import models
from django.conf import settings
from movies.models import Showtime

class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} ({'Booked' if self.is_booked else 'Available'})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(Seat)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('momo', 'Momo'),
        ('cod', 'Cash on Delivery'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.booking.customer.username}"
