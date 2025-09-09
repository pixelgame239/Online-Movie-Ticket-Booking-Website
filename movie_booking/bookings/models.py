from django.db import models
class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)
class Booking(models.Model):
    