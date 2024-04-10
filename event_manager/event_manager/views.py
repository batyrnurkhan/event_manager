from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from events.models import Event
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from events.models import Event, Participant
from django.db import transaction
from event_manager.models import Service

User = get_user_model()  # Get the custom user model


def home(request):
    services = Service.objects.all()[:4]
    return render(request, 'event_manager/home.html', {'page': "Home", 'services': services})


def service_view(request, pk):
    service = Service.objects.get(pk=pk)
    services = Service.objects.exclude(pk=pk)[:4]
    return render(request, 'event_manager/service.html', {'page': "Service", 'services': services, 'service': service})


def portfolio(request):
    return render(request, 'event_manager/portfolio.html', {'page': "Our Portfolio"})


def contact(request):
    return render(request, 'accounts/contact.html', {'page': "Contact Us"})


def budget_calc(request):
    return render(request, 'event_manager/budget_calculator.html', {'page': "Budget Calculator"})


def about_us(request):
    return render(request, 'event_manager/about_us.html', {'page': "About Us"})


from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class GetLogoutView(LogoutView):
    """
    This subclass of LogoutView allows users to log out using a GET request,
    which is necessary if you're using a simple hyperlink for logout.
    """

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    # Optionally, you can specify a page to redirect to after logout.
    next_page = reverse_lazy('home')


from events.models import Participant  # Make sure to import the Participant model


@login_required
def dashboard(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        events = Event.objects.all()
    else:
        # For regular users, filter events they are organizing
        events = Event.objects.filter(event_organizer=request.user)

    today = timezone.localdate()

    # For total tickets sold today, consider only events of interest (filtered by user)
    total_tickets_sold_today = Participant.objects.filter(
        date_joined__date=today,
        event__in=events  # Ensure we're only counting tickets for relevant events
    ).count()

    # Aggregate functions will automatically respect the events queryset filtering
    total_tickets_sold = events.aggregate(Sum('event_sold_tickets'))['event_sold_tickets__sum'] or 0

    # Calculate total profit, considering only the filtered events
    total_profit = sum([event.calculate_profit() for event in events])

    context = {
        'events': events,
        'total_events': events.count(),
        'total_tickets_sold': total_tickets_sold,
        'total_tickets_sold_today': total_tickets_sold_today,
        'total_profit': total_profit,
    }
    return render(request, 'admin/dashboard.html', context)


from accounts.forms import UserSearchForm


@login_required
def event_admin_dashboard(request, slug):
    event = get_object_or_404(Event, event_slug=slug)
    participants = event.participants.all()
    total_earnings = event.event_sold_tickets * event.ticket_cost
    user_search_results = User.objects.none()
    search_form = UserSearchForm(request.GET or None)

    if request.method == 'GET' and search_form.is_valid():
        query = search_form.cleaned_data['query']
        user_search_results = User.objects.filter(username__icontains=query)

    context = {
        'event': event,
        'participants': participants,
        'total_tickets': event.event_tickets,
        'total_earnings': total_earnings,
        'search_form': search_form,
        'user_search_results': user_search_results,
    }
    return render(request, 'admin/event_admin_dashboard.html', context)


@login_required
def add_participant(request, event_slug, user_id):
    event = get_object_or_404(Event, event_slug=event_slug)
    user = get_object_or_404(User, pk=user_id)

    if not request.user.is_staff:
        return HttpResponseForbidden()

    Participant.objects.get_or_create(user=user, event=event)

    return redirect('event_admin_dashboard', slug=event_slug)


@login_required
def remove_participant(request, event_slug, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()  # Ensure only staff can delete participants

    event = get_object_or_404(Event, event_slug=event_slug)
    participant = get_object_or_404(Participant, event=event, user_id=user_id)

    with transaction.atomic():
        # Remove the participant
        participant.delete()

        # Update the Event ticket counts
        event.event_sold_tickets -= 1
        event.event_tickets += 1
        event.event_count_participants -= 1
        event.save()

    return redirect('events:event_admin_dashboard', slug=event_slug)

# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render
# from events.models import Event
#
#
# from django import template
# from events.models import Event
#
# register = template.Library()
#
# @register.inclusion_tag('admin/custom_dashboard.html')  # Make sure this template exists
# def custom_dashboard_data():
#     events = Event.objects.all()
#     events_data = []
#     for event in events:
#         profit = event.event_budget - (event.event_sold_tickets * event.ticket_cost)
#         participants = event.participants.all()
#         events_data.append({
#             'event': event,
#             'profit': profit,
#             'participants': participants,
#         })
#     return {'events_data': events_data}
