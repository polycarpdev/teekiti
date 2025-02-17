from django.contrib import admin
from django.urls import path, include
from users.views import signup, user_login, user_logout
from users.views import AdminLoginView, admin_dashboard
from events.views import event_list
from bookings.views import book_event
# , payment_options, initiate_pesapal_payment_view
from users.views import request_password_reset, verify_otp, reset_password

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('events.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  
    # path('events/', include('events.urls')),
    path('bookings/', include('bookings.urls')), 
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'), 
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('book/<int:event_id>/', book_event, name='book_event'),
    path('password-reset/', request_password_reset, name='password_reset'),
    path('verify-otp/<int:user_id>/', verify_otp, name='verify_otp'),
    path('reset-password/<int:user_id>/', reset_password, name='reset_password'),
    # path('payment/<int:event_id>/', payment_options, name='payment_options'),
    # path('pesapal-pay/<int:event_id>/', initiate_pesapal_payment_view, name='initiate_pesapal_payment'),
    # path('pesapal-callback/', pesapal_callback, name='pesapal_callback'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)