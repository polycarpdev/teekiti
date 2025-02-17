from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, Conference


def test_view(request):
    return HttpResponse("iko sawa buda!")

# listing events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# listing conferences
def conference_list(request):
    conferences  = Conference.objects.all()
    return render(request, 'events/event_list.html', {'conferences': conferences})