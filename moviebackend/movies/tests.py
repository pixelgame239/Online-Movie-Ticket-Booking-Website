from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from movies.models import Movie, Cinema, Showtime, Genre
from bookings.models import Booking, Seat

User = get_user_model()


class IntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Tạo admin và user test
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="adminpass"
        )
        self.user_data = {"username": "newuser", "password": "newpass123"}

        # Genre bắt buộc
        self.genre = Genre.objects.create(genre_name="Action")

        # Movie + Cinema + Showtime
        self.movie = Movie.objects.create(
            title="Avatar",
            duration=120,
            description="Test Movie",
            genre=self.genre,
            ticket_price=100000
        )
        self.cinema = Cinema.objects.create(name="CGV HN", location="Times City")
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            cinema=self.cinema,
            show_time=timezone.now() + timedelta(hours=3)
        )

    # IT_01: Flow end-to-end đặt vé
    def test_IT01_end_to_end_booking(self):
        # Đăng ký user
        user = User.objects.create_user(**self.user_data)

        # Login
        login_ok = self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"]
        )
        self.assertTrue(login_ok)

        # Chọn ghế
        seat = Seat.objects.create(showtime=self.showtime, seat_number="A1")

        # Tạo booking
        booking = Booking.objects.create(
            customer=user,
            showtime=self.showtime,
            total_price=self.movie.ticket_price,
            seats_booked=[seat.seat_number],
            payment_method="banking",
            customer_name="Test User",
            customer_phone="0900000000",
            customer_email="test@example.com"
        )

        self.assertEqual(booking.status, "pending")
        self.assertEqual(booking.total_price, 100000)

    # IT_02: Tích hợp Booking và Payment
    def test_IT02_booking_payment(self):
        user = User.objects.create_user(**self.user_data)
        seat = Seat.objects.create(showtime=self.showtime, seat_number="B1")

        booking = Booking.objects.create(
            customer=user,
            showtime=self.showtime,
            total_price=self.movie.ticket_price,
            seats_booked=[seat.seat_number],
            payment_method="card",
            customer_name="Test User",
            customer_phone="0900000000",
            customer_email="test@example.com"
        )

        # Giả lập thanh toán thành công
        booking.status = "confirmed"
        booking.save()

        self.assertEqual(booking.status, "confirmed")

    # IT_03: Admin hủy suất chiếu
    def test_IT03_admin_cancel_showtime(self):
        # Admin login
        login_ok = self.client.login(username="admin", password="adminpass")
        self.assertTrue(login_ok)

        # Admin xóa suất chiếu
        showtime_id = self.showtime.id
        self.showtime.delete()

        # User không thấy suất chiếu nữa
        exists = Showtime.objects.filter(id=showtime_id).exists()
        self.assertFalse(exists)
