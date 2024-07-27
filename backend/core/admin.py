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















from django.contrib import admin
from .models import SettingModel


class SettingModelAdmin(admin.ModelAdmin):
    list_display = ('bot_username', 'bot_status', 'checker_status', 'auth_status')
    list_filter = ('bot_status', 'checker_status', 'auth_status', 'ir_phone_only', 'auth_phone')
    search_fields = ('bot_username', 'backup_channel', 'bot_token', 'api_id', 'api_hash', 'zarin_key', 'checker_key', 'callino_key')
    ordering = ('bot_username',)
    
    fieldsets = (
        (None, {
            'fields': ('bot_status', 'bot_token', 'api_hash', 'api_id', 'bot_username', 'backup_channel', 'zarin_key', 'checker_key', 'callino_key')
        }),
        ('Status Fields', {
            'fields': ('checker_status', 'auth_status', 'user_limit_pay', 'ir_phone_only', 'auth_phone')
        }),
        ('Text Fields', {
            'fields': ('start_text', 'bot_off_text', 'support_text', 'help_text', 'rule_text', 'join_text', 'user_not_active_text', 'user_profile_text', 'privacy_text', 'approvalـrules', 'inventory_increase_text', 'auth_text', 'auth_phone_text', 'ir_phone_only_text')
        }),
        ('Channels', {
            'fields': ('channel_1', 'channel_2', 'channel_3', 'channel_4', 'channel_5')
        }),
    )

admin.site.register(SettingModel, SettingModelAdmin)