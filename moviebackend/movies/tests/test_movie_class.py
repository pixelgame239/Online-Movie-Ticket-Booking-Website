from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from movies.models import Movie, Cinema, Showtime, Genre
from bookings.models import Booking, Seat