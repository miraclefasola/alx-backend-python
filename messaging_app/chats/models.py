from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_ROLES=[("guest", "Guest"),
               ("host", "Host"),
               ("admin", "Admin")]
    
    user_id= models.UUIDField(default=uuid.uuid4, unique=True, editable= False, db_index=True, primary_key=True )
    first_name= models.CharField(max_length=100, null=False, blank=False)
    last_name= models.CharField(max_length=100, null=False, blank=False)
    email=models.EmailField(unique=True, null=False, blank=False)
    phone_number= models.CharField(max_length=20, unique=True, null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    role= models.CharField(max_length=10, choices=USER_ROLES, default="guest")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Conversation(models.Model):
    conversation_id=models.CharField(default=uuid.uuid4, editable=False, unique=True, null=False, blank=True)
    participants_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name="participants")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Message(models.Model):
    message_id= models.CharField(default=uuid.uuid4, unique=True,editable=False ,null= False,db_index=True, primary_key=True)
    sender_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation_id=models.ForeignKey(Conversation, related_name="conversations", on_delete=models.CASCADE)
    message_body = models.TextField(null=False, blank=True)
    sent_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"