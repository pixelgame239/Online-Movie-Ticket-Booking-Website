from django.contrib import admin
from .models import Movie, Cinema, Showtime

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration', 'release_date')
    search_fields = ('title', 'genre')
    list_filter = ('genre', 'release_date')

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinema', 'show_time')
    list_filter = ('cinema', 'movie')
    search_fields = ('movie__title', 'cinema__name')
