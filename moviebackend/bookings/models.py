from django.db import models
from moviebackend.movies.models import Showtime
from django.contrib.auth.models import User

class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('confirmed','Confirmed'), ('cancelled','Cancelled')])
    booking_date = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=50)  # simulate online payment
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('success','Success'), ('failed','Failed')])
