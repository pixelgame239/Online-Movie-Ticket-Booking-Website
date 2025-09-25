from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from movies.models import Showtime, Movie, Cinema
from .models import Booking, Seat
from .forms import PaymentForm


@login_required
def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seat_numbers = list(range(1, 43))
    booked_seats = Seat.objects.filter(showtime=showtime)
    booked_seat_numbers = [int(seat.seat_number) for seat in booked_seats]

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        payment_method = request.POST.get('payment_method')
        customer_email = request.POST.get('email')
        customer_phone = request.POST.get('phone')

        if not selected_seats:
            messages.error(request, "Bạn phải chọn ít nhất 1 ghế.")
            return redirect('bookings:select_seats', showtime_id=showtime.id)

        # Tạo Booking
        booking = Booking.objects.create(
            customer=request.user,
            showtime=showtime,
            total_price=len(selected_seats) * showtime.movie.ticket_price,
            customer_name=request.user.username,
            customer_email=customer_email,
            customer_phone=customer_phone,
            payment_method=payment_method
        )

        # Đánh dấu ghế
        for seatBooked in selected_seats:
            seat = Seat.objects.create(showtime=showtime, seat_number=int(seatBooked))
            seat.is_booked = True
            seat.save()

        return redirect('bookings:payment', booking_id=booking.id)

    return render(request, 'select_seats.html', {
        'showtime': showtime,
        'seat_numbers': seat_numbers,
        'booked_seat_numbers': booked_seat_numbers
    })


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        method = request.POST.get('method')
        booking.payment_method = method
        booking.status = 'confirmed'
        booking.save()

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

        # Giải phóng ghế
        for seat in Seat.objects.filter(showtime=booking.showtime, is_booked=True):
            seat.is_booked = False
            seat.save()

        messages.success(request, "Hủy vé thành công.")
    else:
        messages.error(request, "Không thể hủy suất chiếu đã qua.")

    return redirect('bookings:booking_history')


@login_required
def my_tickets_view(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'my_tickets.html', {'bookings': bookings})


def buy_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    current_time = timezone.now()

    cinema_ids = Showtime.objects.filter(
        movie=movie,
        show_time__gte=current_time
    ).values_list('cinema_id', flat=True).distinct()
    cinemas = Cinema.objects.filter(id__in=cinema_ids)

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
