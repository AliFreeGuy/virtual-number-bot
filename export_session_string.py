from pyrogram import Client
from os import environ as env


PROXY = {"scheme": 'socks5',
         "hostname": '127.0.0.1',
         "port": 1080}


# BOT
BOT_NAME='virtual-number-bot'
BOT_TOKEN='6273067536:AAF7snU34bPkCRwKxVow-qDRYhjtg5ya_fg'
API_ID='26801362'
API_HASH='ed9c1202ed0cf85a66f8d5b6b392fd1e'
WORK_DIR='/tmp'
BOT_DEBUG='True'






bot = Client('test' , api_id=API_ID , api_hash=API_HASH , bot_token=BOT_TOKEN , proxy=PROXY)

with bot :
    data = bot.export_session_string()
    print(data)