# events/forms.py

from django import forms
from .models import Event
from django.utils import timezone

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(initial=timezone.now(), widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Event
        fields = ['event_name', 'event_sponsor', 'event_description', 'event_budget', 'event_tickets', 'ticket_cost', 'venue', 'start_date', 'event_image']
        widgets = {
            'event_description': forms.Textarea(attrs={'rows': 4}),
        }


class AddParticipantForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)