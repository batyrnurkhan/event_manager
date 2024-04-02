from events.models import Event

def add_event_list_to_context(request):
    return {
        'events': Event.objects.all()
    }
