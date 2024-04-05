from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    email = models.EmailField(max_length=255, unique=True)

class ChatRoom(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')
    created_at = models.DateTimeField(default=timezone.now)

    def get_other_participant(self, user):
        """Return the other participant in a chat room."""
        return self.participants.exclude(id=user.id).first()

    def __str__(self):
        return f"ChatRoom {self.pk} - Participants: {', '.join(participant.username for participant in self.participants.all())}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name