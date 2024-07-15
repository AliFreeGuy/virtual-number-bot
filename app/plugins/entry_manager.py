from pyrogram import Client, filters
from utils import logger , cache 
from utils import filters as f
from utils.connection import connection as con



@Client.on_message(f.updater &f.bot_is_off, group=0)
async def bot_is_off(bot, msg):
    setting = con.setting
    await bot.send_message(msg.from_user.id , setting.bot_off_text)





@Client.on_message(f.updater &f.user_not_active, group=0)
async def user_not_active(bot, msg):
    setting = con.setting
    await bot.send_message(msg.from_user.id , setting.user_not_active_text)


