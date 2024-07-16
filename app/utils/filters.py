from pyrogram import filters
from utils.connection import connection as con 
from utils.logger import logger
import config
from datetime import datetime





async def bot_is_on(_ , cli , msg ):
    setting = con.setting
    if setting.bot_status == True : 
        print('bo on')
        return True
    return False


async def bot_is_off(_ , cli , msg ):
    setting = con.setting
    if setting.bot_status == False :
        print('bo off')

        return True
    return False





async def updater(_ , cli , msg ):
    try :user = con.user(chat_id=msg.from_user.id , full_name=msg.from_user.first_name )
    except Exception as e :logger.warning(e)
    return True




async def user_is_active(_ , cli , msg ):
    user = con.get_user(msg.from_user.id )
    if user.is_active == True  :return True
    return False

async def user_not_active(_ , cli , msg ):
    user = con.get_user(msg.from_user.id )
    if user.is_active is False:return True
    return False



bot_is_on = filters.create(bot_is_on)
bot_is_off = filters.create(bot_is_off)
updater = filters.create(updater)
user_is_active = filters.create(user_is_active)
user_not_active = filters.create(user_not_active)