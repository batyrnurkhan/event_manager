from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView

from .forms import EventForm
from .models import Event
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)
@login_required
def join_event(request, slug):
    logger.debug(f"Attempting to join event with slug: {slug}")
    event = get_object_or_404(Event, event_slug=slug)
    message = event.join_event(request.user)
    messages.add_message(request, messages.INFO, message)
    logger.debug(f"Redirecting to payment for event: {slug}")
    return redirect('events:start_payment', slug=slug)


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
    success_url = reverse_lazy('events/dashboard_event_list')
    template_name = 'events/dashboard_event_confirm_delete.html'

class DashboardEventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/dashboard_event_form.html'
    success_url = reverse_lazy('events:dashboard_event_list')

import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def start_payment(request, slug):
    logger.debug(f"Starting payment process for slug: {slug}")

    event = get_object_or_404(Event, event_slug=slug)

    try:
        # Create a new Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': event.name,
                    },
                    'unit_amount': event.price_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment_success/'),
            cancel_url=request.build_absolute_uri('/payment_cancelled/'),
        )
        logger.debug(f"Redirecting to Stripe Checkout URL: {session.url}")
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, "An error occurred: {}".format(e))
        return redirect('events:event_detail', slug=slug)


from django.shortcuts import render
from django.contrib import messages

def payment_success(request):
    # Logic to handle a successful payment
    # For example, you might want to update an order status in your database
    messages.success(request, "Your payment was successful!")
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    # Logic to handle a cancelled payment
    messages.warning(request, "Your payment was cancelled.")
    return render(request, 'payment_cancelled.html')