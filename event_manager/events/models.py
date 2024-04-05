from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_slug = models.SlugField(max_length=255, unique=True, blank=True)
    event_sponsor = models.CharField(max_length=255)
    event_description = models.TextField()
    event_budget = models.DecimalField(max_digits=10, decimal_places=2)
    event_count_participants = models.PositiveIntegerField(default=0)
    event_tickets = models.PositiveIntegerField()
    event_sold_tickets = models.PositiveIntegerField(default=0)
    event_sold_out = models.BooleanField(default=False)
    event_organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='organized_events')

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_events', blank=True,
                                          through='Participant')
    ticket_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    event_image = models.ImageField(upload_to='events_images/', default='events_images/defaulteventlogo.jpg')
    venue = models.CharField(max_length=255, default='Online')
    start_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.event_slug:
            self.event_slug = slugify(self.event_name)
        super().save(*args, **kwargs)

    def join_event(self, user):
        if self.event_sold_out:
            return "Event is sold out."
        if user in self.participants.all():
            return "User has already joined."
        if self.event_sold_tickets < self.event_tickets:
            self.participants.add(user)
            self.event_count_participants += 1
            self.event_sold_tickets += 1
            self.event_sold_out = self.event_sold_tickets >= self.event_tickets
            self.save()
            return "User joined successfully."
        else:
            self.event_sold_out = True
            self.save()
            return "No more tickets left."

    def calculate_profit(self):
        total_income = self.event_sold_tickets * self.ticket_cost
        profit = total_income - self.event_budget
        return profit

    def __str__(self):
        return f'{self.event_name} - {self.event_budget}'


class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')




@receiver(pre_save, sender=Event)
def slugify_event_name(sender, instance, *args, **kwargs):
    if not instance.event_slug:
        instance.event_slug = slugify(instance.event_name)


from django.core.exceptions import ValidationError

def join_event(self):
    if self.event_sold_out:
        raise ValidationError("Cannot join, event is sold out.")
    if self.event_sold_tickets < self.event_tickets:
        self.event_count_participants += 1
        self.event_sold_tickets += 1
        self.event_sold_out = self.event_sold_tickets >= self.event_tickets
        self.save()
    else:
        self.event_sold_out = True
        self.save()
        raise ValidationError("Cannot join, event tickets are all sold.")