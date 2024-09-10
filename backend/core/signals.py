from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver
from .models import SendMessageModel 
from core.tasks import sendmessage_task 
from accounts.models import User





@receiver(post_save, sender=SendMessageModel)
def print_users(sender, instance, created, **kwargs):

    if created:
        sendmessage_task.delay(instance.id)
        


# @receiver(pre_save, sender=User)
# def wallet_change_notification(sender, instance, **kwargs):
#     if instance.pk:  # بررسی می‌کنیم که آیا این یک رکورد موجود است (در حال به‌روزرسانی)
#         try:
#             previous = User.objects.get(pk=instance.pk)
#             if previous.wallet != instance.wallet:
#                 # اگر مقدار `wallet` تغییر کرده باشد، تسک ارسال پیام را فراخوانی می‌کنیم
#                 send_wallet_update_notification.delay(
#                     chat_id=instance.chat_id,
#                     old_wallet=previous.wallet,
#                     new_wallet=instance.wallet
#                 )
#         except User.DoesNotExist:
#             pass  # در صورت وجود نداشتن کاربر، هیچ عملی انجام نمی‌شو