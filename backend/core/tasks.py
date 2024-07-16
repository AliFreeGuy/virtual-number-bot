
from celery import shared_task
import time
from core.models import SendMessageModel


@shared_task
def sendmessage_task(msg_id):

    msg = SendMessageModel.objects.filter(id = msg_id)

    if msg.exists() :
        msg = msg.first()
        print(msg.user.all())