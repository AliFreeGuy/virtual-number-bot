from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SendMessageModel 
from core.tasks import sendmessage_task







@receiver(post_save, sender=SendMessageModel)
def print_users(sender, instance, created, **kwargs):

    if created:
        sendmessage_task.delay(instance.id)
        



