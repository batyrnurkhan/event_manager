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
    return redirect('events:start_payment', slug=slug)


@login_required
def all_events(request):
    if request.user.is_superuser:
        events = Event.objects.all()
    else:
        # If the user is not a superuser, filter events they are organizing or participating in
        events = Event.objects.filter(event_organizer=request.user) # or use participants for joined events
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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Event.objects.all()
        else:
            return Event.objects.filter(event_organizer=self.request.user)


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
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, "An error occurred: {}".format(e))
        return redirect('events:event_detail', slug=slug)


from django.shortcuts import render
from django.contrib import messages

def payment_success(request):
    # For example, you might want to update an order status in your database
    messages.success(request, "Your payment was successful!")
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    messages.warning(request, "Your payment was cancelled.")
    return render(request, 'payment_cancelled.html')

class MyEventsListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/my_events_list.html'  # ensure this template exists
    context_object_name = 'events'

    def get_queryset(self):
        # Return only events organized by the current user
        return Event.objects.filter(event_organizer=self.request.user)


class MyEventDetailView(DetailView):
    model = Event
    template_name = 'events/my_event_detail.html'
    context_object_name = 'event'
    slug_field = 'event_slug'  # Specify the model's slug field here
    slug_url_kwarg = 'slug'  # The name of the URLconf keyword argument that contains the slug

    def get_object(self, queryset=None):
        # Optionally override this method if more custom behavior is needed
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.get_queryset(), event_slug=slug)

from django.views.generic.edit import UpdateView
from .models import Event
from .forms import EventForm


class MyEventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/my_event_form.html'

    def get_object(self, queryset=None):
        # Use 'event_slug' from the URL to find the Event object
        slug = self.kwargs.get('slug')
        return get_object_or_404(Event, event_slug=slug)

    def get_success_url(self):
        # Dynamically generate the success URL to include the event's slug
        event_slug = self.get_object().event_slug
        return reverse_lazy('events:my_event_detail', kwargs={'slug': event_slug})

from django.http import JsonResponse
from accounts.models import CustomUser
def add_participant_to_event(request, event_slug):
    if request.method == 'POST':
        event = get_object_or_404(Event, event_slug=event_slug)
        # Only allow the event organizer to add participants
        if request.user != event.event_organizer:
            messages.error(request, "You are not authorized to add participants to this event.")
            return redirect('events:my_event_detail', slug=event_slug)

        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            event.participants.add(user)
            messages.success(request, f"{username} has been added as a participant.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")

    return redirect('events:my_event_detail', slug=event_slug)


from django.views.decorators.http import require_POST


@login_required
def remove_participant(request, event_slug, user_id):
    event = get_object_or_404(Event, event_slug=event_slug, event_organizer=request.user)
    user = get_object_or_404(CustomUser, id=user_id)

    # Check if the user is the event organizer
    if request.user == event.event_organizer:
        if user in event.participants.all():
            event.participants.remove(user)
            # Decrement the event_count_participants and event_sold_tickets here
            event.event_count_participants = max(0, event.event_count_participants - 1)
            event.event_sold_tickets = max(0, event.event_sold_tickets - 1)
            event.event_sold_out = False  # Optionally reconsider the sold out status
            event.save()

    return redirect('events:my_event_detail', slug=event_slug)


def event_search(request):
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(event_name__icontains=query).values('event_name', 'event_description',
                                                                          'event_slug')  # Adjust fields as necessary
    else:
        events = Event.objects.none().values('event_name', 'event_description', 'event_slug')

    events_list = list(events)
    return JsonResponse({'events': events_list})