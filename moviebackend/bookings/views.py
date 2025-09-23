from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from movies.models import Showtime, Movie
from .models import Booking, Seat


@login_required
def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = showtime.seats.all().order_by('seat_number')

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        if not selected_seats:
            messages.error(request, "You must select at least one seat")
            return redirect('bookings:select_seats', showtime_id=showtime.id)

        booking = Booking.objects.create(
            customer=request.user,
            showtime=showtime,
            total_price=len(selected_seats) * 100.00  # giá demo
        )

        for seat_num in selected_seats:
            seat = Seat.objects.get(showtime=showtime, seat_number=seat_num)
            if seat.is_booked:
                messages.error(request, f"Seat {seat_num} already booked")
                booking.delete()
                return redirect('bookings:select_seats', showtime_id=showtime.id)

            seat.is_booked = True
            seat.save()

            # Tạo Ticket gắn seat này vào booking
            Booking.objects.create(
                booking=booking,
                showtime=showtime,
                seat=seat,
                price=100.00  # giá demo, có thể lấy từ showtime
            )

        return redirect('bookings:payment', booking_id=booking.id)

    return render(request, 'select_seats.html', {'showtime': showtime, 'seats': seats})


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        method = request.POST.get('method')
        Booking.objects.create(
            booking=booking,
            method=method,
            amount=booking.total_price,
            status='success'
        )
        messages.success(request, "Payment successful!")
        return redirect('bookings:booking_history')

    return render(request, 'payment.html', {'booking': booking})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'booking_history.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if booking.showtime.show_time > timezone.now():
        booking.status = 'cancelled'
        booking.save()

        # Giải phóng ghế từ ticket
        for ticket in booking.tickets.all():
            seat = ticket.seat
            seat.is_booked = False
            seat.save()

        messages.success(request, "Booking cancelled successfully")
    else:
        messages.error(request, "Cannot cancel past showtime")

    return redirect('bookings:booking_history')
@login_required
def my_tickets_view(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'my_tickets.html', {'bookings': bookings})

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from movies.models import Movie, Showtime, Cinema  # adjust if needed

def buy_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    current_time = timezone.now()

    # Get all cinemas with upcoming showtimes for this movie
    cinema_ids = Showtime.objects.filter(
        movie=movie,
        show_time__gte=current_time
    ).values_list('cinema_id', flat=True).distinct()
    cinemas = Cinema.objects.filter(id__in=cinema_ids)

    # Optional: filter showtimes by selected cinema
    selected_cinema_id = request.GET.get('cinema')
    showtimes = Showtime.objects.filter(
        movie=movie,
        show_time__gte=current_time
    )
    if selected_cinema_id:
        showtimes = showtimes.filter(cinema_id=selected_cinema_id)

    showtimes = showtimes.order_by('show_time')

    return render(request, 'buy_ticket.html', {
        'movie': movie,
        'cinemas': cinemas,
        'showtimes': showtimes,
        'selected_cinema_id': int(selected_cinema_id) if selected_cinema_id else None
    })

