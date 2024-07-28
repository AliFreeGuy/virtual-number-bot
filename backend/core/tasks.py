
from celery import shared_task
import time
from pyrogram import Client 
from django.conf import settings
from core.models import SendMessageModel , SettingModel
from os import environ as env
from accounts.models import User
import logging


PROXY = {"scheme": 'socks5',
            "hostname": '127.0.0.1',
            "port": 1080}



@shared_task
def sendmessage_task(msg_id):

    msg = SendMessageModel.objects.filter(id = msg_id)
    setting = SettingModel.objects.first()
    if msg.exists() :
        msg = msg.first()

        
        if msg.for_all :users = User.objects.all()
        else : users = msg.user.all()
        
        if settings.DEBUG  : bot = Client('message-sender' , api_hash=setting.api_hash , api_id=setting.api_id , bot_token=setting.bot_token , proxy=PROXY)
        else :bot = Client('message-sender' , api_hash=setting.api_hash , api_id=setting.api_id , bot_token=setting.bot_token)

        for user in users :
        
            with bot :

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
def send_message(status , chat_id  , amount     ):
    setting = SettingModel.objects.first()
    if settings.DEBUG  : bot = Client('send_message' , api_hash=setting.api_hash , api_id=setting.api_id , bot_token=setting.bot_token , proxy=PROXY)
    else :bot = Client('send_message' , api_hash=setting.api_hash , api_id=setting.api_id , bot_token=setting.bot_token)


    if status == 'ok' :
        success_message = f'با موفقیت مقدار {str(amount)} تومان حساب شما شارژ شد !'
        chat_link =  f"tg://openmessage?user_id={str(chat_id)}"
    
        bakcup_text = f'''
✅ پرداخت موفق

کاربر : [ {str(chat_id)} ]({chat_link})
مقدار شارژ : {amount}
'''


        with bot :
            bot.send_message(chat_id = chat_id , text = success_message)
            bot.send_message(chat_id=int(setting.backup_channel ) , text =bakcup_text )