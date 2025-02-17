from django.db import models
from django.conf import settings
from events.models import Event

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"



class Payment(models.Model):
    PAYMENT_METHODS = [
        ('PESAPAL', 'PesaPal'),
        ('MPESA', 'M-Pesa'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_code = models.CharField(max_length=255, unique=True)  # PesaPal tracking ID or M-Pesa code
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')  # e.g., COMPLETED, FAILED

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"