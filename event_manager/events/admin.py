from django.contrib import admin
from .models import Event
from event_manager.models import Service


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_sponsor', 'tickets_sold_out', 'remaining_budget')

    @admin.display(description='Tickets Sold Out')
    def tickets_sold_out(self, obj):
        return obj.event_sold_tickets >= obj.event_tickets

    @admin.display(description='Remaining Budget')
    def remaining_budget(self, obj):
        spent = obj.ticket_cost * obj.event_count_participants
        return obj.event_budget - spent


admin.site.register(Service)
