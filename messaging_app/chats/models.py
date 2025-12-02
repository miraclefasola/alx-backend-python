from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLES = [("guest", "Guest"), ("host", "Host"), ("admin", "Admin")]

    user_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
    )
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default="guest")
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    # Alx instruction requires us to include password but django already handles that

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, null=False, blank=True
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" ID: {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        null=False,
        db_index=True,
        primary_key=True,
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}: {self.message_body[:20]}"
