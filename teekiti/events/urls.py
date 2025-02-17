from django.urls import path
from .views import test_view, event_list

urlpatterns = [
    path('test/', test_view, name='test'),
    path('', event_list, name='event_list'),
]