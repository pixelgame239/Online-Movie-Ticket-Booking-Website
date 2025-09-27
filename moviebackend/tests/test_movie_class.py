from django.test import TestCase, Client
from datetime import date
from movies.models import Movie, Cinema, Showtime, Genre
from bookings.models import Booking, Seat
from django.db.utils import IntegrityError

class MovieModelTests(TestCase):
    
    def setUp(self):
        self.genre = Genre.objects.create(genre_name='Action')

    def test_movie_create_success(self):
        movie = Movie.objects.create(
            title="Test Movie",
            genre=self.genre,
            duration=120,
            description="A test movie",
            release_date=date(2023, 1, 1),
            ticket_price=100000,
        )
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.genre.genre_name, "Action")
        self.assertEqual(movie.duration, 120)
        self.assertEqual(movie.description, "A test movie")
        self.assertEqual(movie.release_date, date(2023, 1, 1))
        self.assertEqual(movie.ticket_price, 100000)

    def test_movie_create_fail_without_genre(self):
        with self.assertRaises(IntegrityError):
            Movie.objects.create(
                title="Invalid Movie",
                duration=100,
                description="This should fail",
                release_date=date(2023, 2, 1),
                ticket_price=100000,
            )
    
    def test_movie_create_fail_with_invalid_genre(self):
        with self.assertRaises(ValueError):
            Movie.objects.create(
                title="Invalid Movie",
                genre="Romance",
                duration=100,
                description="This should fail",
                release_date=date(2023, 2, 1),
                ticket_price=100000,
            )
    def test_movie_partial_update_success(self):
        movie = Movie.objects.create(
            title="Old Movie",
            genre=self.genre,
            duration=100,
            description="An old movie",
            release_date=date(2020, 1, 1),
            ticket_price=100000,
        )

        movie.title = "Updated Movie"
        movie.save()

        updated_movie = Movie.objects.get(id=movie.id)
        self.assertEqual(updated_movie.title, "Updated Movie")
    def test_movie_update_success(self):
        newGenre = Genre.objects.create(genre_name="Romance")
        movie = Movie.objects.create(
            title="Old Movie",
            genre=self.genre,
            duration=100,
            description="An old movie",
            release_date=date(2020, 1, 1),
            ticket_price=100000,
        )

        movie.title = "Updated Movie"
        movie.genre=newGenre
        movie.duration=120
        movie.description="New movie"
        movie.release_date=date(2022,1,1)
        movie.ticket_price=90000

        movie.save()

        updated_movie = Movie.objects.get(id=movie.id)
        self.assertEqual(updated_movie.title, "Updated Movie")
        self.assertEqual(updated_movie.genre.genre_name, "Romance")
        self.assertEqual(updated_movie.duration,120)
        self.assertEqual(updated_movie.description, "New movie")
        self.assertEqual(updated_movie.release_date, date(2022,1,1))
        self.assertEqual(updated_movie.ticket_price, 90000)
    def test_movie_update_fail_with_invalid_genre_name(self):
        movie = Movie.objects.create(
            title="Old Movie",
            genre=self.genre,
            duration=100,
            description="An old movie",
            release_date=date(2020, 1, 1),
            ticket_price=100000,
        )
        with self.assertRaises(Genre.DoesNotExist):
            invalid_genre = Genre.objects.get(genre_name="Fighting")
            movie.genre = invalid_genre
            movie.save()

    def test_delete_movie_success(self):
        movie = Movie.objects.create(
            title="Movie to delete",
            genre=self.genre,
            duration=90,
            description="A movie to be deleted",
            release_date=date(2022, 1, 1),
            ticket_price=100000,
        )
        movie_id = movie.id
        movie.delete()

        with self.assertRaises(Movie.DoesNotExist):
            Movie.objects.get(id=movie_id)
    def test_delete_movie_fail_no_record(self):
        with self.assertRaises(Movie.DoesNotExist):
            movie = Movie.objects.get(id=999)
            movie.delete()