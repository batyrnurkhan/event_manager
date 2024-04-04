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

##########################
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Event
from .forms import EventForm
class AddEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/dashboard_event_form.html'
    success_url = reverse_lazy('events:dashboard_event_list')  # Adjust this to your actual success URL

    def form_valid(self, form):
        form.instance.event_organizer = self.request.user  # Set the organizer to the current user
        return super().form_valid(form)

from django.views.generic import ListView
from .models import Event

class DashboardEventListView(ListView):
    model = Event
    template_name = 'events/dashboard_event_list.html'
    context_object_name = 'events'


from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from .forms import EventForm  # Ensure you have created an EventForm as previously discussed
from django.utils import timezone
from datetime import timedelta
class DashboardEventDetailView(DetailView):
    model = Event
    template_name = 'events/dashboard_event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context['event']
        tickets_sold_last_24h = event.participants.filter(date_joined__gte=timezone.now() - timedelta(days=1)).count()
        total_tickets_sold = event.event_sold_tickets
        earnings = event.calculate_profit()
        profit = event.calculate_profit()

        context['profit'] = profit
        context['tickets_sold_last_24h'] = tickets_sold_last_24h
        context['total_tickets_sold'] = total_tickets_sold
        context['earnings'] = earnings
        participants = event.participants.all()
        context['participants'] = participants

        return context

class DashboardEventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('events:dashboard_event_list')
    template_name = 'events/dashboard_event_confirm_delete.html'

class DashboardEventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/dashboard_event_form.html'
    success_url = reverse_lazy('events:dashboard_event_list')