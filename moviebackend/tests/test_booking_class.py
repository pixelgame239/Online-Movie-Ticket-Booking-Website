from django.test import TestCase
from django.contrib.auth import get_user_model
from bookings.models import Booking, Seat
from movies.models import Genre, Movie, Cinema, Showtime
from datetime import datetime, timedelta

User = get_user_model()

class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.genre = Genre.objects.create(genre_name='Action')
        self.movie = Movie.objects.create(
            title='Test Movie',
            genre=self.genre,
            duration=120,
            ticket_price=75000
        )
        self.cinema = Cinema.objects.create(name='Cinema 1', location='Location A')
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            cinema=self.cinema,
            show_time=datetime.now() + timedelta(days=1)
        )

    def test_seat_booking_and_total_price_success(self):
        seats = ['1', '2', '3']
        booking = Booking.objects.create(
            customer=self.user,
            showtime=self.showtime,
            total_price=len(seats) * self.movie.ticket_price,
            customer_name="Test User",
            customer_email="test@example.com",
            customer_phone="0123456789",
            seats_booked=seats,
            payment_method='card'
        )

        for seat in seats:
            Seat.objects.create(showtime=self.showtime, seat_number=seat, is_booked=True)

        self.assertEqual(booking.total_price, 225000)
        self.assertEqual(booking.seats_booked, ["1","2","3"])

        booked = Seat.objects.filter(showtime=self.showtime, is_booked=True)
        self.assertEqual(booked.count(), 3)

    def test_booking_fails_when_seat_is_already_booked(self):
        Seat.objects.create(showtime=self.showtime, seat_number='5', is_booked=True)

        seats = ['5', '6']

        with self.assertRaises(Exception):
            for seat in seats:
                if Seat.objects.filter(showtime=self.showtime, seat_number=seat, is_booked=True).exists():
                    raise Exception(f"Seat {seat} is already booked.")
                Seat.objects.create(showtime=self.showtime, seat_number=seat, is_booked=True)

    def test_duplicate_seat_booking_same_user_should_overwrite(self):
        first_booking = Booking.objects.create(
            customer=self.user,
            showtime=self.showtime,
            total_price=1 * self.movie.ticket_price,
            customer_name="Test User",
            customer_email="test@example.com",
            customer_phone="0123456789",
            seats_booked=['9'],
            payment_method='card'
        )
        Seat.objects.create(showtime=self.showtime, seat_number='9', is_booked=True)

        Seat.objects.filter(showtime=self.showtime, seat_number='9').delete()
        first_booking.seats_booked = ['10']
        first_booking.total_price = self.movie.ticket_price
        first_booking.save()
        Seat.objects.create(showtime=self.showtime, seat_number='10', is_booked=True)

        self.assertTrue(Seat.objects.filter(showtime=self.showtime, seat_number='10', is_booked=True).exists())
        self.assertFalse(Seat.objects.filter(showtime=self.showtime, seat_number='9').exists())
        self.assertEqual(first_booking.seats_booked, ['10'])

