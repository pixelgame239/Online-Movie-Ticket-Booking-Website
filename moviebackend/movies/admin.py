from django.contrib import admin
from .models import Movie, Cinema, Showtime, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name',)
    search_fields = ('genre_name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration', 'release_date', 'ticket_price', 'buy_count')
    search_fields = ('title', 'genre__genre_name')
    list_filter = ('genre', 'release_date')
    readonly_fields = ('buy_count',)


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinema', 'show_time')
    list_filter = ('cinema', 'movie')
    search_fields = ('movie__title', 'cinema__name')
