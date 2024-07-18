from django.contrib import admin
from .models import SettingModel , SendMessageModel 
from jdatetime import datetime as jdatetime_datetime




class SendMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_all', 'text', 'jalali_creation')
    list_filter = ('for_all', 'creation')
    search_fields = ('text',)
    filter_horizontal = ('user',)

    def jalali_creation(self, obj):
        if obj.creation:
            jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
            return jalali_date
        else:
            return '-'
    jalali_creation.short_description = 'Creation'

admin.site.register(SendMessageModel, SendMessageModelAdmin)
















class SettingModelAdmin(admin.ModelAdmin):
    # نمایش فیلدهای مدل در لیست ادمین
    list_display = (
        'bot_status', 'bot_token', 'api_hash', 'api_id', 'bot_username',
        'backup_channel', 'zarin_key', 'checker_key', 'checker_status', 
        'auth_status', 'user_limit_pay'
    )
    
    # امکان جستجو بر اساس فیلدهای خاص
    search_fields = ('bot_username', 'backup_channel')
    
    # فیلتر کردن بر اساس فیلدهای خاص
    list_filter = ('bot_status', 'checker_status', 'auth_status')
    
    # نمایش تمام فیلدها در یک گروه در فرم ادمین
    fieldsets = (
        ('Bot Setting', {
            'fields': (
                'bot_status', 'bot_token', 'api_hash', 'api_id', 'bot_username',
                'backup_channel', 'zarin_key', 'checker_key', 'checker_status', 
                'auth_status', 'user_limit_pay', 'start_text', 'bot_off_text', 
                'support_text', 'help_text', 'rule_text', 'join_text', 
                'user_not_active_text', 'user_profile_text', 'channel_1', 
                'channel_2', 'channel_3', 'channel_4', 'channel_5'
            )
        }),
    )

admin.site.register(SettingModel, SettingModelAdmin)
