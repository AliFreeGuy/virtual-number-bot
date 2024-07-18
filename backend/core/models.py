from django.db import models
from accounts.models import User
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
    checker_status = models.BooleanField()
    auth_status = models.BooleanField(default=False)
    user_limit_pay = models.BigIntegerField()


    start_text = models.TextField()
    bot_off_text = models.TextField()
    support_text = models.TextField()
    help_text = models.TextField()
    rule_text = models.TextField()
    join_text = models.TextField()
    user_not_active_text = models.TextField()
    user_profile_text = models.TextField()
    privacy_text = models.TextField(default='none')


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


