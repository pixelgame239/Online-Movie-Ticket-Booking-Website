from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from movies.models import Genre, Movie, Cinema, Showtime
from bookings.models import Seat, Booking

User = get_user_model()

class UnitTestCases(TestCase):
    def setUp(self):
        # Tạo user
        self.user = User.objects.create_user(username="user", password="123456789")

        # Tạo genre, movie, cinema, showtime
        genre = Genre.objects.create(genre_name="Action")
        self.movie = Movie.objects.create(
            title="Movie A",
            genre=genre,
            duration=120,
            ticket_price=100,
        )
        self.cinema = Cinema.objects.create(name="Cinema 1", location="HN")
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            cinema=self.cinema,
            show_time=timezone.now() + timezone.timedelta(hours=2)
        )

        # Ghế cho suất chiếu
        self.seat_b5 = Seat.objects.create(showtime=self.showtime, seat_number="B5", is_booked=False)
        self.seat_b6 = Seat.objects.create(showtime=self.showtime, seat_number="B6", is_booked=True)

        # Booking pending ban đầu
        self.booking = Booking.objects.create(
            customer=self.user,
            showtime=self.showtime,
            total_price=0,
            status="pending",
            seats_booked=[],
            payment_method="banking",
            customer_name="User",
            customer_phone="0912345678",
            customer_email="user@gmail.com"
        )

    # UT_01: Tính tổng giá vé hợp lệ (3 vé)
    def test_UT01_calculate_total_price_valid(self):
        total = self.movie.ticket_price * 3
        self.assertEqual(total, 300)

    # UT_02: Tính tổng giá vé không giảm giá (2 vé)
    def test_UT02_calculate_total_price_no_discount(self):
        total = self.movie.ticket_price * 2
        self.assertEqual(total, 200)

    # UT_03: Kiểm tra ghế còn trống
    def test_UT03_validate_seat_available(self):
        self.assertFalse(self.seat_b5.is_booked)

    # UT_04: Kiểm tra ghế đã đặt
    def test_UT04_validate_seat_booked(self):
        self.assertTrue(self.seat_b6.is_booked)

    # UT_05: Đăng nhập hợp lệ
    def test_UT05_login_valid(self):
        login = self.client.login(username="user", password="123456789")
        self.assertTrue(login)

    # UT_06: Đăng nhập sai mật khẩu
    def test_UT06_login_invalid_password(self):
        login = self.client.login(username="user", password="sai")
        self.assertFalse(login)

    # UT_07: Cập nhật trạng thái đặt vé
    def test_UT07_update_booking_status(self):
        self.booking.status = "confirmed"
        self.booking.save()
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")
