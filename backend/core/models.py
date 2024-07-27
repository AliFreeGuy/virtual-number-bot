from django.db import models
from accounts.models import User
import random
# Create your models here.


class SettingModel(models.Model):

    bot_status = models.BooleanField(default=True)
    bot_token = models.CharField(max_length=128)
    api_hash = models.CharField(max_length=128)
    api_id  = models.CharField(max_length=128)
    bot_username = models.CharField(max_length=128)
    backup_channel = models.BigIntegerField()
    zarin_key = models.CharField(max_length=256)
    checker_key = models.CharField(max_length=256)
    callino_key = models.CharField(max_length=256 , default='none')
    checker_status = models.BooleanField()
    auth_status = models.BooleanField(default=False)
    user_limit_pay = models.BigIntegerField()
    ir_phone_only = models.BooleanField(default=False)
    auth_phone = models.BooleanField(default=False)

    start_text = models.TextField(default='متن استارت')
    bot_off_text = models.TextField(default='متن ربات خاموش')
    support_text = models.TextField(default='متن پشتیبانی')
    help_text = models.TextField(default='متن راهنما')
    rule_text = models.TextField(default='متن قوانین')
    join_text = models.TextField(default='متن جوین اجباری')
    user_not_active_text = models.TextField(default='متن کاربر غیر فعال')
    user_profile_text = models.TextField(default='متن زیر پروفایل کاربر')
    privacy_text = models.TextField(default='متن حریم خصوصی')
    approvalـrules = models.TextField(default='متن تایید قوانین ')
    inventory_increase_text = models.TextField(default='متن افزایش موجودی')
    auth_text = models.TextField(default='متن احراز هویت')
    auth_phone_text = models.TextField(default='متن تایید شماره تلفن')
    ir_phone_only_text = models.TextField(default='متن افزایش موجودی فقط با شماره ایرانی')
    inventory_transfer_text = models.TextField(default='متن انتقال موجودی')
    inventory_transfer_error_text = models.TextField(default='متن خطایه انتقال موجودی')
    inventory_transfer_amount_text = models.TextField(default='متن مقدار انتقال موجودی')



    channel_1 = models.CharField(max_length=256  , null=True , blank=True)
    channel_2 = models.CharField(max_length=256, null=True , blank=True)
    channel_3 = models.CharField(max_length=256, null=True , blank=True)
    channel_4 = models.CharField(max_length=256, null=True , blank=True)
    channel_5 = models.CharField(max_length=256, null=True , blank=True)



    def __str__(self) -> str:
        return self.bot_username
    


    class Meta :
        verbose_name = "Setting"
        verbose_name_plural = "Setting"









class InventoryTransferModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.PositiveBigIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    tracking_code = models.CharField(max_length=6, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            tracking_code = random.randint(11111 , 999999)
            while InventoryTransferModel.objects.filter(tracking_code=tracking_code).exists():
                tracking_code = random.randint(11111 , 999999)
            self.tracking_code = tracking_code
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Transfer of {self.amount} from {self.sender} to {self.receiver} on {self.creation_date} with tracking code {self.tracking_code}"



class SendMessageModel(models.Model):
    user = models.ManyToManyField(User, related_name='admin_message', blank=True)
    text = models.TextField()
    creation = models.DateTimeField(auto_now_add=True)
    for_all = models.BooleanField(default=True)

    def __str__(self):
        return str(self.text[:30])

    class Meta:
        verbose_name = "SendMessage"
        verbose_name_plural = "SendMessages"


