from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from movies.models import Showtime, Movie, Cinema
from .models import Booking, Seat
from users.models import User

def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seat_numbers = list(range(1, 43))
    customer_name = request.user.username if request.user.is_authenticated else 'Guest'
    customer_email = request.user.email if request.user.is_authenticated else ''
    customer_phone = request.user.phone if request.user.is_authenticated else ''
    if(request.user.is_authenticated):
        prev_booking = Booking.objects.filter(showtime=showtime, customer=request.user).first()
        prev_booking_seats = prev_booking.seats_booked if prev_booking else []
    else:
        prev_booking_seats=[]
    booked_seats = Seat.objects.filter(showtime=showtime).exclude(seat_number__in=prev_booking_seats)
    booked_seat_numbers = [int(seat.seat_number) for seat in booked_seats]
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        print(request.POST)
        payment_method  = request.POST['payment_method']
        print(selected_seats)
        if not selected_seats:
            messages.error(request, "Bạn phải chọn ít nhất 1 ghế.")
            return redirect('bookings:select_seats', showtime_id=showtime.id)
        customer_user = request.user if request.user.is_authenticated else User.objects.get(id=2)
        if len(prev_booking_seats)==0:
            booking = Booking.objects.create(
                customer=customer_user,
                showtime=showtime,
                total_price=len(selected_seats) * showtime.movie.ticket_price, 
                customer_name= request.POST['customer_name'],
                customer_email = request.POST['customer_email'],
                customer_phone = request.POST['customer_phone'],
                seats_booked=selected_seats,
                payment_method=payment_method
            )
        else:
            booking = prev_booking 
            Seat.objects.filter(
                showtime=showtime,
                seat_number__in=booking.seats_booked
            ).delete()
            booking.seats_booked = selected_seats
            booking.total_price = len(selected_seats) * showtime.movie.ticket_price
            booking.payment_method = payment_method
            booking.customer_name = request.POST['customer_name']
            booking.customer_email = request.POST['customer_email']
            booking.customer_phone = request.POST['customer_phone']
            booking.save()

        # Đánh dấu ghế
        for seatBooked in selected_seats:
            Seat.objects.create(showtime=showtime, seat_number=seatBooked, is_booked=True)

        return redirect('bookings:booking_completed')

    return render(request, 'select_seats.html', {
        'showtime': showtime,
        'seat_numbers': seat_numbers,
        'booked_seat_numbers': booked_seat_numbers,  # Pass booked seat numbers to the template
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'prev_selected_seats': prev_booking_seats,
    })


def booking_completed(request):
    return render(request, 'booking_completed.html')

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'booking_history.html', {'bookings': bookings})


@login_required
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        showtime_id = request.POST.get('showtime_id')
        booking = get_object_or_404(Booking, id=booking_id, showtime = showtime_id, customer=request.user)
        seat_numbers = booking.seats_booked
        Seat.objects.filter(
            showtime=booking.showtime,
            seat_number__in=seat_numbers
        ).delete()
        booking.status = 'cancelled'
        booking.save()
        return redirect('bookings:my_tickets')

    return redirect('bookings:my_tickets')

def my_tickets_view(request):
    if(request.user.is_authenticated):
        bookings = Booking.objects.filter(customer=request.user)
        return render(request, 'my_tickets.html', {'bookings': bookings})
    else:
        return render(request, 'login.html')

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
