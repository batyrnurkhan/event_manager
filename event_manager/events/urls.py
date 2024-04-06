from django.urls import path
from .views import all_events, event_detail, join_event, AddEventView, \
    start_payment, payment_success, payment_cancelled  # Make sure to define add_event view
from .views import (DashboardEventListView, DashboardEventDetailView,
                    DashboardEventDeleteView, DashboardEventUpdateView)
app_name = 'events'

urlpatterns = [
    path('', all_events, name='all_events'),
    path('add/', AddEventView.as_view(), name='add_event'),
    path('join/<slug:slug>/', join_event, name='join_event'),
    path('payment/<slug:slug>/', start_payment, name='start_payment'),
    path('<slug:slug>/', event_detail, name='event_detail'),

    path('payment_success/', payment_success, name='payment_success'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),

    path('dashboard/events/', DashboardEventListView.as_view(), name='dashboard_event_list'),
    path('dashboard/events/<int:pk>/', DashboardEventDetailView.as_view(), name='dashboard_event_detail'),
    path('dashboard/events/<int:pk>/delete/', DashboardEventDeleteView.as_view(), name='dashboard_event_delete'),
    path('dashboard/events/<int:pk>/edit/', DashboardEventUpdateView.as_view(), name='dashboard_event_edit'),
]