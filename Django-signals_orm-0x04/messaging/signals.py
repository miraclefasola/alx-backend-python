from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification
from django.contrib.auth import get_user_model


User = get_user_model


@receiver(post_save, sender=Message, dispatch_uid="notis")
def create_notification(sender, instance, created, **kwargs):
    """Create a notification for the receiver when a new message is sent."""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)