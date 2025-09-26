from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Movie, Genre, Cinema, Showtime

class MovieAppTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Genre
        cls.genre1 = Genre.objects.create(genre_name="Hài")
        cls.genre2 = Genre.objects.create(genre_name="Hành động")

        # Movie
        cls.movie1 = Movie.objects.create(
            title="Funny Movie",
            genre=cls.genre1,
            duration=90,
            release_date=timezone.now().date()
        )
        cls.movie2 = Movie.objects.create(
            title="Action Movie",
            genre=cls.genre2,
            duration=120,
            release_date=timezone.now().date()
        )

        # Cinema
        cls.cinema1 = Cinema.objects.create(
            name="CGV Vincom",
            location="Hà Nội",
            phone_number="0123456789"
        )

        cls.cinema2 = Cinema.objects.create(
            name="Lotte Cinema",
            location="HCM",
            phone_number="0987654321"
        )

        # Showtime
        cls.showtime1 = Showtime.objects.create(
            movie=cls.movie1,
            cinema=cls.cinema1,
            show_time=timezone.now() + timedelta(hours=2)
        )
        cls.showtime2 = Showtime.objects.create(
            movie=cls.movie2,
            cinema=cls.cinema2,
            show_time=timezone.now() + timedelta(days=1)
        )

    # TC1: Trang home hiển thị phim đang chiếu
    def test_home_view_shows_now_showing_movies(self):
        response = self.client.get(reverse('movies:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie1.title)
        self.assertContains(response, self.movie2.title)

    # TC2: Trang home hiển thị top 3 phim hot
    def test_home_view_shows_movies_hot(self):
        # Tăng buy_count để movie1 trở thành hot
        self.movie1.buy_count = 10
        self.movie1.save()
        response = self.client.get(reverse('movies:home'))
        self.assertContains(response, self.movie1.title)

    # TC3: Trang danh sách phim hiển thị tất cả movies
    def test_movie_list_view_displays_all_movies(self):
        response = self.client.get(reverse('movies:movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie1.title)
        self.assertContains(response, self.movie2.title)

    # TC4: Search movie theo title
    def test_movie_list_search_by_title(self):
        response = self.client.get(reverse('movies:movie_list'), {'q': 'Funny'})
        self.assertContains(response, self.movie1.title)
        self.assertNotContains(response, self.movie2.title)

    # TC5: Filter movie theo genre
    def test_movie_list_filter_by_genre(self):
        response = self.client.get(reverse('movies:movie_list'), {'genre': 'Hành động'})
        self.assertContains(response, self.movie2.title)
        self.assertNotContains(response, self.movie1.title)
