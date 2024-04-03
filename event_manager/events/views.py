from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView

from .forms import EventForm
from .models import Event
from django.contrib import messages

@login_required
def join_event(request, slug):
    event = get_object_or_404(Event, event_slug=slug)
    message = event.join_event(request.user)
    messages.add_message(request, messages.INFO, message)
    return redirect('events:event_detail', slug=slug)

def all_events(request):
    events = Event.objects.all()  # Retrieve all events
    return render(request, 'event_manager/home.html', {'events': events})

def event_detail(request, slug):
    event = get_object_or_404(Event, event_slug=slug)
    tickets_left = event.event_tickets - event.event_sold_tickets
    context = {
        'event': event,
        'tickets_left': tickets_left,
    }
    return render(request, 'events/event_detail.html', context)


class AddEventView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'  # Template to render the form
    success_url = '/'