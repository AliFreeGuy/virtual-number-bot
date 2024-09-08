from django.db import models
from accounts.models import User
import random
# Create your models here.




class SettingModel(models.Model):

    STATUS_CHOICES = [
        ('active', 'فعال ها'),
        ('inactive', 'غیر فعال ها'),
        ('all', 'همه'),
    ]
    bot_status = models.BooleanField(default=True)
    bot_token = models.CharField(max_length=128)
    api_hash = models.CharField(max_length=128)
    api_id  = models.CharField(max_length=128)
    session_string = models.TextField(default='none')
    bot_username = models.CharField(max_length=128)
    backup_channel = models.BigIntegerField()
    zarin_key = models.CharField(max_length=256)
    checker_key = models.CharField(max_length=256)
    callino_key = models.CharField(max_length=256 , default='none')
    checker_status = models.BooleanField()
    auto_checker  = models.PositiveIntegerField(default=1)
    auth_status = models.BooleanField(default=False)
    user_limit_pay = models.BigIntegerField()
    ir_phone_only = models.BooleanField(default=False)
    auth_phone = models.BooleanField(default=False)
    interest_rates = models.PositiveBigIntegerField(default=0)
    number_rows = models.PositiveBigIntegerField(default=10)
    number_timeout = models.PositiveIntegerField(default=5)
    show_numbers = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='all',
    )

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
    get_user_amount_text = models.TextField(default='متن ارسال مقدار شارژ حساب')
    auth_text = models.TextField(default='متن احراز هویت')
    send_auth_data_text = models.TextField(default='متن ارسال مدارک احراز هویت')
    received_auth_text =models.TextField(default='متن مدارک شما دریافت شد')
    auth_phone_text = models.TextField(default='متن تایید شماره تلفن')
    ir_phone_only_text = models.TextField(default='متن افزایش موجودی فقط با شماره ایرانی')
    inventory_transfer_text = models.TextField(default='متن انتقال موجودی')
    inventory_transfer_error_text = models.TextField(default='متن خطایه انتقال موجودی')
    inventory_transfer_amount_text = models.TextField(default='متن مقدار انتقال موجودی')
    payment_description = models.TextField(default='متن صفحه درگاه پرداخت')
    buy_number_text = models.TextField(default='متن خرید شماره مجازی')
    send_number_to_user_text = models.TextField(default='متن هنگام ارسال شماره به کاربر ')
    user_no_inventory = models.TextField(default='متن کاربر موجودی ندارد !')



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





class UserPaymentModel(models.Model):
    user  = models.ForeignKey(User , on_delete=models.CASCADE , related_name='payments')
    status = models.BooleanField(default=False)
    amount = models.BigIntegerField()
    key = models.CharField(max_length=300)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{str(self.user)} - {str(self.amount)} - {str(self.status)}'
    
    class Meta:
                verbose_name = "UserPaymnet"
                verbose_name_plural = "UserPaymnet"



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
    
    class Meta:
            verbose_name = "InventoryTransfer"
            verbose_name_plural = "InventoryTransfer"


class NumbersModel(models.Model):
    weight = models.IntegerField(default=1)
    name = models.CharField(max_length=128)
    default_price = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()
    status = models.BooleanField(default=True)
    range = models.IntegerField(default=0)  # افزودن فیلد range
    emoji = models.CharField(max_length=10, blank=True)  # افزودن فیلد emoji
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['price', '-weight'] 
        verbose_name = "Numbers"
        verbose_name_plural = "Numbers"



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





class UserOrdersModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    country = models.ForeignKey(NumbersModel, on_delete=models.CASCADE, related_name='orders')
    number = models.CharField(max_length=55)
    price = models.PositiveIntegerField()
    request_id = models.PositiveIntegerField(default=0  , unique=True)
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
