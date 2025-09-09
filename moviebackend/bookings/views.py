from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Showtime, Seat
from .models import Booking, Payment
from .forms import PaymentForm
from django.contrib import messages
from django.utils import timezone

@login_required
def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = showtime.seats.all().order_by('seat_number')
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        if not selected_seats:
            messages.error(request, "You must select at least one seat")
            return redirect('select_seats', showtime_id=showtime.id)
        
        booking = Booking.objects.create(
            customer=request.user,
            showtime=showtime,
            total_price=len(selected_seats)*100.00  
        )
        for seat_num in selected_seats:
            seat = Seat.objects.get(showtime=showtime, seat_number=seat_num)
            if seat.is_booked:
                messages.error(request, f"Seat {seat_num} already booked")
                booking.delete()
                return redirect('select_seats', showtime_id=showtime.id)
            seat.is_booked = True
            seat.save()
            booking.seats.add(seat)
        return redirect('payment', booking_id=booking.id)
    
    return render(request, 'bookings/select_seats.html', {'showtime': showtime, 'seats': seats})

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        method = request.POST.get('method')
        Payment.objects.create(
            booking=booking,
            method=method,
            amount=booking.total_price,
            status='success' 
        )
        messages.success(request, "Payment successful!")
        return redirect('booking_history')
    return render(request, 'bookings/payment.html', {'booking': booking})

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.showtime.show_time > timezone.now():
        booking.status = 'cancelled'
        booking.save()
        for seat in booking.seats.all():
            seat.is_booked = False
            seat.save()
        messages.success(request, "Booking cancelled successfully")
    else:
        messages.error(request, "Cannot cancel past showtime")
    return redirect('booking_history')
