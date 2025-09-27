from django.contrib import admin
from .models import Movie, Cinema, Showtime, Genre
from django.utils.html import format_html
from django import forms
from utils.supabase import upload_to_supabase
import os, uuid


class MovieAdminForm(forms.ModelForm):
    upload_poster = forms.ImageField(
        required=False,
        help_text="Upload a poster image (stored in Supabase)"
    )

    class Meta:
        model = Movie
        exclude = ('poster', )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Ưu tiên upload file
        upload = self.cleaned_data.get("upload_poster")
        if upload:
            ext = os.path.splitext(upload.name)[1]
            fileName = f"{uuid.uuid4().hex}{ext}"
            movieBytes = upload.read()
            url = upload_to_supabase(
                movieBytes,
                path_in_bucket=fileName,
                bucket_name="movies"
            )
            instance.poster = url
        elif self.cleaned_data.get("poster_url"):
            # Nếu không upload file thì lấy URL
            instance.poster = self.cleaned_data["poster_url"]

        if commit:
            instance.save()
        return instance


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name',)
    search_fields = ('genre_name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    list_display = ('title', 'genre', 'duration', 'release_date', 'ticket_price', 'buy_count', 'poster_preview')
    readonly_fields = ('buy_count', 'poster_preview')

    def poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="height:100px; max-width:70px;" />', obj.poster)
        return "No poster"
    poster_preview.short_description = "Poster"


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'cinema', 'show_time')
    list_filter = ('cinema', 'movie')
    search_fields = ('movie__title', 'cinema__name')
