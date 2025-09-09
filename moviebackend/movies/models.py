from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    duration = models.IntegerField()  
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/')

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
