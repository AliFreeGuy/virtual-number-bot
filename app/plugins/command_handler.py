from pyrogram import Client, filters
from utils import logger , cache 
from utils import filters as f
from utils.connection import connection as con

@Client.on_message(f.updater &f.bot_is_on & f.user_is_active, group=1)
async def command_manager(bot, msg):
    

    if msg and msg.text :


        if msg.text == '/privacy' :
            setting  = con.setting
            await bot.send_message(msg.from_user.id , setting.privacy_text)