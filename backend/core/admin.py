from django.contrib import admin
from .models import SettingModel

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
