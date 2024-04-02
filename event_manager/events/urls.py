from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.all_events, name='all_events'),
    path('join/<slug:slug>/', views.join_event, name='join_event'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
]
