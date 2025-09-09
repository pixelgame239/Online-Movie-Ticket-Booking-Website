from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='showtimes')
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} - {self.show_time}"
