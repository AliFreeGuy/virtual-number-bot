
from celery import shared_task
import time
from pyrogram import Client 
from django.conf import settings
from core.models import SendMessageModel , SettingModel , NumbersModel
from os import environ as env
from accounts.models import User
from django.core.management.base import BaseCommand
import logging
import json
import jdatetime
from datetime import datetime
import requests



PROXY = {"scheme": 'socks5',
            "hostname": '127.0.0.1',
            "port": 1080}




# تنظیمات لاگینگ
# تنظیمات لاگینگ
logger = logging.getLogger(__name__)

@shared_task
def number_task():
    messages = []
    
    # دریافت کلید از مدل تنظیمات
    setting = SettingModel.objects.first()
    if not setting:
        print("تنظیمات یافت نشد.")
        return
    
    # درخواست به API
    url = f'https://api.ozvinoo.xyz/web/{setting.callino_key}/get-prices/1'
    res = requests.get(url=url)
    
    if res.status_code == 200:
        api_data = res.json()
    else:
        message = f"خطا در درخواست به API: {res.status_code}"
        messages.append(message)
        logger.error(message)
        print(message)
        return

    # دریافت لیست کشورها از مدل
    existing_countries = NumbersModel.objects.all()
    existing_countries_dict = {country.name: country for country in existing_countries}
    
    # آماده‌سازی داده‌های API برای به‌روزرسانی مدل
    api_countries_dict = {}
    for item in api_data:
        country_name = item['country']
        default_price = item['price']
        price = item['price']
        range_value = item.get('range', 0)  # دریافت مقدار range
        emoji = item.get('emoji', '')  # دریافت مقدار emoji
        api_countries_dict[country_name] = {
            'default_price': default_price,
            'price': price,
            'status': item['count'] == '✅ موجود',
            'range': range_value,
            'emoji': emoji
        }
    
    # بررسی و بروزرسانی کشورها
    for country_name, api_info in api_countries_dict.items():
        if country_name in existing_countries_dict:
            country = existing_countries_dict[country_name]
            # بررسی تغییر قیمت پیش‌فرض
            if country.default_price != api_info['default_price']:
                old_price = country.default_price
                country.default_price = api_info['default_price']
                country.save()
                message = f"قیمت پیش‌فرض {country_name} تغییر کرده است: قیمت قبلی {old_price}، قیمت جدید {api_info['default_price']}."
                messages.append(message)
               
            
            # بررسی تغییر قیمت
            # if country.price != api_info['price']:
            #     old_price = country.price
            #     country.price = api_info['price']
            #     country.save()
            #     message = f"قیمت {country_name} تغییر کرده است: قیمت قبلی {old_price}، قیمت جدید {api_info['price']}."
            #     messages.append(message)
               
            
            # بررسی تغییر وضعیت
            if country.status != api_info['status']:
                country.status = api_info['status']
                country.save()
                status_message = "موجود" if api_info['status'] else "ناموجود"
                message = f"وضعیت {country_name} تغییر کرده است: وضعیت جدید {status_message}."
                messages.append(message)
              
            
            # بررسی تغییر range
            if country.range != api_info['range']:
                country.range = api_info['range']
                country.save()
                message = f"مقدار range {country_name} تغییر کرده است: مقدار جدید {api_info['range']}."
                messages.append(message)
                
            
            # بررسی تغییر emoji
            if country.emoji != api_info['emoji']:
                country.emoji = api_info['emoji']
                country.save()
                message = f"ایموجی {country_name} تغییر کرده است: ایموجی جدید {api_info['emoji']}."
                messages.append(message)
            
        else:
            # کشور جدید است
            message = f"کشور {country_name} اضافه شده است."
            messages.append(message)
            logger.info(message)
            NumbersModel.objects.create(
                name=country_name,
                default_price=api_info['default_price'],
                price=api_info['price'],
                status=api_info['status'],
                range=api_info['range'],
                emoji=api_info['emoji']
            )
    
    # کشورهایی که در API نیستند اما در مدل موجود هستند به غیر فعال تغییر داده می‌شوند
    for country_name, country in existing_countries_dict.items():
        if country_name not in api_countries_dict:
            message = f"کشور {country_name} حذف شده است."
            messages.append(message)
            country.status = False
            country.save()
    
    # چاپ تمام پیام‌های ذخیره شده
    numbers_log.delay(messages)




@shared_task
def numbers_log(messages):
    now = datetime.now()
    shamsi_date = jdatetime.date.fromgregorian(date=now).strftime('%Y-%m-%d')
    shamsi_time = now.strftime('%H:%M:%S')
    timestamp = f"{shamsi_date} {shamsi_time}"
    setting = SettingModel.objects.first()
    if settings.DEBUG  : bot = Client('test' , api_hash=setting.api_hash , api_id=setting.api_id , session_string=setting.session_string)
    else :bot = Client('test' , api_hash=setting.api_hash , api_id=setting.api_id , session_string=setting.session_string)
    for message in messages :
        with bot :
            bot.send_message(int(setting.backup_channel) , text = f'{message}\n\n{timestamp}')




@shared_task
def sendmessage_task(msg_id):

    msg = SendMessageModel.objects.filter(id = msg_id)
    setting = SettingModel.objects.first()
    if msg.exists() :
        msg = msg.first()

        
        if msg.for_all :users = User.objects.all()
        else : users = msg.user.all()
        
        if settings.DEBUG  : bot = Client('message-sender' , api_hash=setting.api_hash , api_id=setting.api_id , session_string=setting.session_string)
        else :bot = Client('message-sender' , api_hash=setting.api_hash , api_id=setting.api_id , session_string=setting.session_string)
        with bot :
            for user in users :
                if msg.text.startswith('https://t.me/c/') :
                    try : 
                        msg_id = msg.text.split('/')[-1]
                        chat_id = f'-100{msg.text.split("/")[-2]}'
                        message = bot.get_messages(chat_id=int(chat_id) , message_ids=int(msg_id))
                        message.copy(int(user.chat_id))
                    except Exception as e :logging.warning(e)

                elif msg.text.startswith('https://t.me/') :
                    try : 
                        msg_id = msg.text.split('/')[-1]
                        chat_id = f'{msg.text.split("/")[-2]}'
                        message = bot.get_messages(chat_id=chat_id , message_ids=int(msg_id))
                        message.copy(int(user.chat_id))
                    except Exception as e :logging.warning(e)

                else :
                    try : bot.send_message(chat_id=int(user.chat_id)  , text = msg.text)
                    except Exception as e :logging.warning(e)
            



@shared_task
def send_message(status, chat_id, amount, previous_balance, date):
    setting = SettingModel.objects.first()
    user = User.objects.get(chat_id=chat_id)
    if settings.DEBUG:
        bot = Client('send_message', api_hash=setting.api_hash, api_id=setting.api_id, session_string=setting.session_string)
    else:
        bot = Client('send_message', api_hash=setting.api_hash, api_id=setting.api_id, session_string=setting.session_string)

    if status == 'ok':
        success_message = f'با موفقیت مقدار {str(amount)} تومان حساب شما شارژ شد !'
        chat_link = f"tg://openmessage?user_id={str(chat_id)}"
        
        # تبدیل تاریخ ایجاد به شمسی
        creation_date_jalali = jdatetime.datetime.fromgregorian(datetime=date).strftime('%Y/%m/%d %H:%M:%S')
        
        backup_text = f'''
✅ پرداخت موفق

کاربر : [ {str(chat_id)} ]({chat_link})
مقدار شارژ : {amount}
تاریخ : {creation_date_jalali}
موجودی قبلی : {previous_balance}
موجودی جدید : {str(user.wallet)}
'''

        with bot:
            # bot.send_message(chat_id=chat_id, text=success_message)
            bot.send_message(chat_id=int(setting.backup_channel), text=backup_text)



@shared_task
def send_wallet_update_notification(chat_id, old_wallet, new_wallet):
    setting = SettingModel.objects.first()
    user = User.objects.get(chat_id=chat_id)

    # تنظیمات کلاینت بر اساس وضعیت DEBUG
    bot = Client(
        'wallet_update_notification',
        api_hash=setting.api_hash,
        api_id=setting.api_id,
        session_string=setting.session_string
    )

    # محاسبه تغییر موجودی
    difference = new_wallet - old_wallet
    
    # دریافت زمان و تاریخ کنونی میلادی
    current_time = jdatetime.datetime.now().strftime('%H:%M:%S, [%Y/%m/%d %I:%M %p]')
    
    # دریافت زمان و تاریخ کنونی شمسی
    current_time_jalali = jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    
    if difference > 0:
        # اگر موجودی افزایش یافته باشد
        update_message = f'''
✅ با موفقیت حساب شما {difference} تومن شارژ شد
💰 موجودی قبلی : {old_wallet}
💎 موجودی جدید : {new_wallet}
'''
    else:
        # اگر موجودی کاهش یافته باشد
        update_message = f'''
✅ با موفقیت حساب شما {abs(difference)} تومن کسر شد
💰 موجودی قبلی : {old_wallet}
💎 موجودی جدید : {new_wallet}
'''

    # پیام به کانال پشتیبان شامل اطلاعات تغییر موجودی با تاریخ شمسی
    backup_text = f'''
🛠️ تغییر موجودی

کاربر: {user.chat_id}
موجودی قبلی: {old_wallet} تومان
موجودی جدید: {new_wallet} تومان
{"🔺 افزایش" if difference > 0 else "🔻 کاهش"}: {abs(difference)} تومان
📅 تاریخ: {current_time_jalali} 
'''

    with bot:
        # ارسال پیام تغییر به کاربر
        bot.send_message(chat_id=chat_id, text=update_message)
        # ارسال اطلاعات تغییر موجودی به کانال پشتیبان
        bot.send_message(chat_id=int(setting.backup_channel), text=backup_text)
