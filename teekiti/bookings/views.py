from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.models import Event
from .models import Booking, Event, Payment
# from .pesapal import initiate_pesapal_payment
from django.urls import reverse
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



@login_required(login_url='/login/')
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        if seats <= event.available_seats:
            # Create booking
            Booking.objects.create(
                user=request.user,
                event=event,
                seats_booked=seats
            )
            # Update available seats
            event.available_seats -= seats
            event.save()
            messages.success(request, "Booking successful!")
            return redirect('event_list')
        else:
            messages.error(request, "Not enough seats available.")
    return render(request, 'bookings/book_event.html', {'event': event})



