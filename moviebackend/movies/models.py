from django.db import models

class Genre(models.Model):
    genre_name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.genre_name
    
class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="movies")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    poster = models.URLField(blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=7, decimal_places=0, help_text="Price for watching at the cinema", default=0)
    buy_count = models.PositiveIntegerField(help_text="Amount of tickets sold for this movie", default=0)

    def __str__(self):
        return self.title

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='showtimes')
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} - {self.show_time}"
