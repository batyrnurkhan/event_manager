from django.urls import path
from .views import all_events, event_detail, join_event, AddEventView  # Make sure to define add_event view

app_name = 'events'

urlpatterns = [
    path('', all_events, name='all_events'),
    path('join/<slug:slug>/', join_event, name='join_event'),
    path('<slug:slug>/', event_detail, name='event_detail'),
    path('add/', AddEventView.as_view(), name='add_event'),  # URL for adding a new event
]