from pyrogram import Client, filters
from utils import logger , cache 
from utils import filters as f
from utils.connection import connection as con

@Client.on_message(f.updater , group=0)
async def command_manager(bot, msg):
    setting = con.setting
    print(setting)
    await bot.send_message(msg.from_user.id , f'hi user')