from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from events.models import Event
from bookings.models import Booking
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import CustomUser, PasswordResetOTP
from django.contrib.auth import get_user_model

# Signup View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send email with credentials


            send_mail(
                'Your Teekiti Login Details',
                f'Username: {user.username}\nPassword: {form.cleaned_data["password1"]}\nPhone No.:{user.phone_number}',
                # Phone No.:{user.phone_number}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('login')  # Redirect to login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # Check if the user is an admin
                messages.error(request, "Admins must use the admin login page.")
                return redirect('login')  # Redirect back to user login
            login(request, user)  # Log in regular users
            return redirect('event_list')
    else:
        form = AuthenticationForm(request)
    return render(request, 'users/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect('event_list')  # Redirect to event list after logout


# ADMIN LOGIN
class AdminLoginView(LoginView):
    template_name = 'users/admin_login.html'

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')  # Redirect to admin dashboard after login

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:  # Block non-admin users
            messages.error(self.request, "You are not an admin.")
            return redirect('admin_login')
        return super().form_valid(form)
    

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    User = get_user_model()
    user_count = User.objects.count()
    booking_count = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(total=Sum('event__price'))['total'] or 0

    context = {
        'user_count': user_count,
        'booking_count': booking_count,
        'total_revenue': total_revenue,
    }
    return render(request, 'admin/dashboard.html', context)




def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = PasswordResetOTP.objects.create(user=user)
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp.otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp', user_id=user.id)
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user with this email exists.')
    return render(request, 'users/password_reset_request.html')

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if PasswordResetOTP.objects.filter(user=user, otp=otp).exists():
            return redirect('reset_password', user_id=user.id)
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'users/verify_otp.html')

def reset_password(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        user.set_password(password)
        user.save()
        messages.success(request, 'Password reset successful. Login with new password.')
        return redirect('login')
    return render(request, 'users/reset_password.html')